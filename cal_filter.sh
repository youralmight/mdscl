#!/usr/bin/env bash
# 从源日历筛事件，全量重建到目标日历。
#
#   ./cal_filter.sh [-n] <源日历> <目标日历> <PCRE>
#
#   -n   dry run，只打印会做什么，不动任何日历
#
# 每次跑都是全量重建：先清空目标日历，再把源日历里匹配的事件加进去。
# 跑两次结果一样。源日历一个字都不动。
#
# 正则走 grep -P（PCRE），匹配对象是每个事件的
#     标题 <TAB> 地点 <TAB> 描述
# 拼成的一行。不含日期、id、日历名——那些不参与匹配。
# 事件描述里的换行会被 gcalcli 转义成字面的 \n，所以一个事件永远是一行。
#
# 重复事件会被展开成一个个独立事件。gcalcli 读不出 RRULE
# （agenda --details 的可选值里根本没有 recurrence），所以保不住重复规则。
# 每周一次上 5 周的课，目标日历里就是 5 个独立事件。
#
# 时间范围默认 1970-01-01 → 2099-12-31，即"全部历史 + 未来"。
# 用 CAL_START / CAL_END 环境变量可以改。
#
# 依赖 gcalcli。第一次用之前要先授权：
#     uvx --from gcalcli gcalcli init
# 授权信息存在 ~/Library/Application Support/gcalcli/，uvx 每次跑都能读到。

set -euo pipefail

GCALCLI="${GCALCLI:-uvx --from gcalcli gcalcli}"
START="${CAL_START:-1970-01-01}"
END="${CAL_END:-2099-12-31}"

# macOS 自带的是 BSD grep，没有 -P。按顺序找一个真能跑 PCRE 的：
#   GNU grep -P（Linux 默认，或 brew install grep 装的 ggrep）→ pcre2grep
# 三个都没有就直接退，不偷偷降级成 -E——那会让正则语义悄悄变掉。
if echo x | grep -qP x 2>/dev/null;       then GREP_P=(grep -nP)
elif echo x | ggrep -qP x 2>/dev/null;    then GREP_P=(ggrep -nP)
elif command -v pcre2grep >/dev/null;     then GREP_P=(pcre2grep -n)
else
  echo "找不到支持 PCRE 的 grep。装一个：brew install grep（然后用 ggrep）或 brew install pcre2" >&2
  exit 1
fi

dry=0
if [[ ${1:-} == -n ]]; then dry=1; shift; fi

if [[ $# -ne 3 ]]; then
  sed -n '2,26p' "$0" >&2
  exit 1
fi
src="$1"; dst="$2"; re="$3"

tsv="$(mktemp)"; match="$(mktemp)"; keep="$(mktemp)"
trap 'rm -f "$tsv" "$match" "$keep"' EXIT

# ---- 1. 读源日历 ----------------------------------------------------------
# --tsv 会先打一行表头，下面靠表头按列名定位，不硬编码列序。
echo ">>> 读 [$src] $START → $END"
$GCALCLI --calendar "$src" agenda --tsv --details all "$START" "$END" > "$tsv"

n_total=$(( $(wc -l < "$tsv") - 1 ))
[[ $n_total -lt 0 ]] && n_total=0
echo "    $n_total 个事件"

# ---- 2. 拼出用来匹配的文本，一行一个事件 ----------------------------------
awk -F'\t' '
  NR==1 { for (i=1; i<=NF; i++) col[$i]=i; next }
  { printf "%s\t%s\t%s\n", $col["title"], $col["location"], $col["description"] }
' "$tsv" > "$match"

# ---- 3. grep -P 筛，拿行号 ------------------------------------------------
# 空结果时 grep 返回 1，不能让 set -e 把脚本干掉。
"${GREP_P[@]}" -- "$re" "$match" | cut -d: -f1 > "$keep" || true
n_keep=$(wc -l < "$keep" | tr -d ' ')
echo ">>> 正则 /$re/ 命中 $n_keep / $n_total"

if [[ $n_keep -eq 0 ]]; then
  echo "    一个都没匹配上，不动目标日历，退出。" >&2
  exit 1
fi

if [[ $dry -eq 1 ]]; then
  echo ">>> dry run，下面是会被复制过去的事件："
  awk -F'\t' -v keepfile="$keep" '
    BEGIN { while ((getline l < keepfile) > 0) k[l]=1 }
    NR==1 { for (i=1; i<=NF; i++) col[$i]=i; next }
    k[NR-1] { printf "    %s %s  %s\n", $col["start_date"], $col["start_time"], $col["title"] }
  ' "$tsv"
  echo ">>> 目标日历 [$dst] 未改动。"
  exit 0
fi

# ---- 4. 清空目标日历 ------------------------------------------------------
# gcalcli 没有"清空"这个操作，delete 必须收一个搜索词。
# 空串它会直接报错（源码里写死了 "The empty string would get *ALL* events"），
# 但一个空格是 truthy，能过检查，然后原样传给 Google 的 q= 参数。
# --iamaexpert 跳过逐个确认。
echo ">>> 清空 [$dst]"
$GCALCLI --calendar "$dst" delete --iamaexpert " " "$START" "$END"

# ---- 5. 逐个加到目标日历 --------------------------------------------------
# 不用 bash 的 IFS=$'\t' read：连续 tab 会被折叠成一个，空的 location
# 或 description 会让后面所有列串位。改用 NUL 分隔。
echo ">>> 写入 [$dst]"
i=0
while IFS= read -r -d '' title &&
      IFS= read -r -d '' loc   &&
      IFS= read -r -d '' desc  &&
      IFS= read -r -d '' sd    &&
      IFS= read -r -d '' st    &&
      IFS= read -r -d '' ed    &&
      IFS= read -r -d '' et; do
  args=(--calendar "$dst" add --noprompt --title "$title")
  [[ -n "$loc"  ]] && args+=(--where "$loc")
  [[ -n "$desc" ]] && args+=(--description "$desc")

  if [[ -z "$st" ]]; then
    # 全天事件：gcalcli 输出的 end_date 是 Google 的排他式结束日，原样传回去
    args+=(--allday --when "$sd" --end "$ed")
  else
    args+=(--when "$sd $st" --end "$ed $et")
  fi

  $GCALCLI "${args[@]}" >/dev/null
  i=$((i+1))
  printf '\r    %d / %d' "$i" "$n_keep"
done < <(
  awk -F'\t' -v keepfile="$keep" '
    BEGIN { while ((getline l < keepfile) > 0) k[l]=1; ORS="" }
    NR==1 { for (i=1; i<=NF; i++) col[$i]=i; next }
    k[NR-1] {
      printf "%s%c%s%c%s%c%s%c%s%c%s%c%s%c",
        $col["title"],       0, $col["location"],   0, $col["description"], 0,
        $col["start_date"],  0, $col["start_time"], 0,
        $col["end_date"],    0, $col["end_time"],   0
    }
  ' "$tsv"
)
printf '\n'
echo "全部成功：$n_keep 个事件已重建到 [$dst]"
