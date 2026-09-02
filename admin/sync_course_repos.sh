#!/usr/bin/env bash
# 一键同步仓库：自动发现组织下的新仓库 → clone 新的 → 按 mode 更新已有的。
#
# 两种 mode（在 sources.conf 里每条来源自己指定）：
#
#   mirror  只读镜像。上游经常 reset/rebase 改历史，所以不用 pull，
#           直接 fetch + reset --hard 到远端，本地改动一律丢弃。
#           → 课程根 official/current，未建课程则进 admin/upstream/current
#
#   work    自己要动手的。只 clone 新的 + fetch，绝不碰工作区和当前分支。
#           远端默认分支动了会提示，但要不要合并由你自己决定。
#           → 课程根 assignments/<kind>
#
# 来源配置：admin/sources.conf
#           name ; api_base ; org ; include ; exclude ; family ; mode
# 名单快照：admin/<family>.txt（每次自动重写，进 git）
# 克隆目标：按 family 和 repo 名路由
#
# 凭据：从 ~/.git-credentials 按 API 主机名取 token（私有 org 必须有）。
#
#   admin/sync_course_repos.sh                 # 全部来源：发现 + 同步
#   admin/sync_course_repos.sh assignments     # 只同步某一条来源
#   admin/sync_course_repos.sh --offline       # 不查 API，直接按现有名单同步
#   admin/sync_course_repos.sh --list-only     # 只刷新名单，不 clone/更新
#   admin/sync_course_repos.sh --clean         # mirror 源顺便删掉未跟踪文件（不影响 work 源）
set -uo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
conf="$script_dir/sources.conf"
[[ -f "$conf" ]] || { echo "缺来源配置: $conf" >&2; exit 1; }

offline=0
list_only=0
do_clean=0
wanted=()
for a in "$@"; do
  case "$a" in
    --offline)   offline=1 ;;
    --list-only) list_only=1 ;;
    --clean)     do_clean=1 ;;
    -h|--help)   sed -n '2,31p' "$0"; exit 0 ;;
    -*)          echo "未知参数: $a" >&2; exit 1 ;;
    *)           wanted+=("$a") ;;
  esac
done

trim() { local s="$1"; s="${s#"${s%%[![:space:]]*}"}"; printf '%s' "${s%"${s##*[![:space:]]}"}"; }

# 从 ~/.git-credentials 取某主机的 token
token_for() {
  python3 - "$1" <<'PY'
import sys, os, urllib.parse
host = sys.argv[1]
path = os.path.expanduser("~/.git-credentials")
if os.path.exists(path):
    for line in open(path):
        u = urllib.parse.urlsplit(line.strip())
        if u.hostname == host and u.password:
            print(urllib.parse.unquote(u.password)); break
PY
}

# 分页拉取 org 下所有 repo 的 clone_url，按 include / exclude 过滤，追加进 $tmp
discover() {
  local api="$1" org="$2" inc="$3" exc="$4" host tok
  host="$(python3 -c 'import sys,urllib.parse;print(urllib.parse.urlsplit(sys.argv[1]).hostname)' "$api")"
  tok="$(token_for "$host")"
  local page=1 body n
  while :; do
    body="$(curl -sS --fail-with-body \
      ${tok:+-H "Authorization: token $tok"} \
      -H "Accept: application/vnd.github+json" \
      "$api/orgs/$org/repos?per_page=100&page=$page")" || { echo "API 失败: $api/orgs/$org" >&2; return 1; }
    n="$(INC="$inc" EXC="$exc" python3 -c '
import json,sys,os,re
d=json.load(sys.stdin)
inc,exc=os.environ["INC"],os.environ["EXC"]
rs=[r for r in d
    if (not inc or re.search(inc, r["name"]))
    and (not exc or not re.search(exc, r["name"]))]
for r in sorted(rs, key=lambda x: x["name"]): print(r["clone_url"])
print(len(d), file=sys.stderr)
' <<<"$body" 2>&1 >>"$tmp")" || return 1
    [[ "$n" -lt 100 ]] && break
    page=$((page+1))
  done
}

# 远端默认分支（origin/HEAD）。上游换过默认分支也能跟上。
remote_head() {
  local d="$1" h
  h="$(git -C "$d" symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null)"
  if [[ -z "$h" ]]; then
    git -C "$d" remote set-head origin -a >/dev/null 2>&1
    h="$(git -C "$d" symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null)"
  fi
  [[ -z "$h" ]] && h="origin/$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null)"
  echo "$h"
}

course_prefix() {
  local repo="$1"
  if [[ "$repo" =~ ^(DSCI|COLX)_[0-9]{3} ]]; then
    printf '%s' "${BASH_REMATCH[0]}"
  fi
}

assignment_kind() {
  local repo="$1"
  if [[ "$repo" =~ ^(DSCI|COLX)_[0-9]{3}_(.+)_yz2000$ ]]; then
    printf '%s' "${BASH_REMATCH[2]}"
  fi
}

active_course() {
  local course="$1"
  [[ -n "$course" && -d "$repo_root/$course" ]]
}

repo_dest() {
  local family="$1" repo="$2" course kind
  course="$(course_prefix "$repo")"
  case "$family" in
    current)
      if active_course "$course"; then
        printf '%s/%s/official/current/%s' "$repo_root" "$course" "$repo"
      else
        printf '%s/admin/upstream/current/%s' "$repo_root" "$repo"
      fi
      ;;
    public)
      if active_course "$course"; then
        printf '%s/%s/official/public/%s' "$repo_root" "$course" "$repo"
      else
        printf '%s/admin/upstream/public/%s' "$repo_root" "$repo"
      fi
      ;;
    work)
      kind="$(assignment_kind "$repo")"
      [[ -n "$course" && -n "$kind" ]] || { echo "无法路由作业仓库: $repo" >&2; return 1; }
      printf '%s/%s/assignments/%s/%s' "$repo_root" "$course" "$kind" "$repo"
      ;;
    *)
      echo "未知 family: $family" >&2
      return 1
      ;;
  esac
}
failed=()

# mirror：强制对齐远端，本地改动丢弃
update_mirror() {
  local dir="$1" url="$2" repo="$3" head old new dirty
  head="$(remote_head "$dir")"
  old="$(git -C "$dir" rev-parse HEAD 2>/dev/null)"
  new="$(git -C "$dir" rev-parse "$head" 2>/dev/null)"
  [[ -z "$new" ]] && { echo ">>> $repo 找不到远端分支 ($head)"; failed+=("head $url"); return; }

  if [[ "$old" != "$new" ]]; then
    if git -C "$dir" merge-base --is-ancestor "$old" "$new" 2>/dev/null; then
      echo ">>> 更新 $repo  ($(git -C "$dir" rev-list --count "$old..$new") 个新提交)"
    else
      echo ">>> 【历史被改写】$repo  ${old:0:8} → ${new:0:8}，强制对齐"
    fi
    git -C "$dir" reset -q --hard "$new" || { failed+=("reset $url"); return; }
  fi

  dirty="$(git -C "$dir" status --porcelain)"
  if [[ -n "$dirty" ]]; then
    if [[ $do_clean -eq 1 ]]; then
      echo "    清理未跟踪/修改的文件"
      git -C "$dir" reset -q --hard "$new"; git -C "$dir" clean -qfd
    else
      echo "    ⚠ $repo 有本地改动（--clean 可清掉）："
      sed 's/^/      /' <<<"$dirty" | head -5
    fi
  fi
}

# work：只把远端抓下来，工作区和当前分支一个字都不动
update_work() {
  local dir="$1" url="$2" repo="$3" head old new branch behind
  head="$(remote_head "$dir")"
  new="$(git -C "$dir" rev-parse "$head" 2>/dev/null)"
  [[ -z "$new" ]] && return

  branch="$(git -C "$dir" rev-parse --abbrev-ref HEAD 2>/dev/null)"
  old="$(git -C "$dir" rev-parse HEAD 2>/dev/null)"

  if [[ "$old" != "$new" ]] && ! git -C "$dir" merge-base --is-ancestor "$new" "$old" 2>/dev/null; then
    behind="$(git -C "$dir" rev-list --count "$old..$new" 2>/dev/null)"
    echo ">>> $repo  远端 $head 有 ${behind} 个新提交（你在 $branch）"
    echo "    要合并自己来：git -C '$dir' merge $head"
  fi
}

while IFS=';' read -r name api org inc exc family mode; do
  name="$(trim "${name:-}")"
  [[ -z "$name" || "$name" == \#* ]] && continue
  api="$(trim "${api:-}")";  org="$(trim "${org:-}")"
  inc="$(trim "${inc:-}")";  exc="$(trim "${exc:-}")"
  family="$(trim "${family:-}")"; mode="$(trim "${mode:-mirror}")"

  [[ -n "$family" ]] || { echo "来源 $name 没写 family" >&2; failed+=("family $name"); continue; }
  case "$mode" in
    mirror|work) ;;
    *) echo "来源 $name 的 mode 不认识: $mode（只能是 mirror 或 work）" >&2; failed+=("mode $name"); continue ;;
  esac

  if [[ ${#wanted[@]} -gt 0 ]]; then
    printf '%s\n' "${wanted[@]}" | grep -qx "$name" || continue
  fi

  list="$script_dir/$family.txt"

  if [[ $offline -eq 0 ]]; then
    tmp="$(mktemp)"
    if discover "$api" "$org" "$inc" "$exc"; then
      if [[ -f "$list" ]] && ! diff -q "$list" "$tmp" >/dev/null; then
        echo "### $name 名单变化："
        diff "$list" "$tmp" | sed -n 's/^> /  + /p;s/^< /  - /p'
      fi
      mkdir -p "$(dirname "$list")"
      mv "$tmp" "$list"
    else
      rm -f "$tmp"
      echo "!!! $name 发现失败，回退到现有名单" >&2
      failed+=("discover $name")
    fi
  fi

  [[ -f "$list" ]] || { echo "名单不存在: $list" >&2; failed+=("missing $name"); continue; }
  [[ $list_only -eq 1 ]] && continue

  repo_count="$(python3 - "$list" <<'PY'
import sys

with open(sys.argv[1]) as fh:
    print(sum(1 for line in fh if line.strip() and not line.lstrip().startswith("#")))
PY
)"
  echo "=== $name [$mode/$family] ($repo_count 个仓库)"
  while read -r url; do
    [[ -z "$url" || "$url" == \#* ]] && continue
    repo="$(basename "$url" .git)"
    dir="$(repo_dest "$family" "$repo")" || { failed+=("route $url"); continue; }
    mkdir -p "$(dirname "$dir")"

    if [[ ! -d "$dir/.git" ]]; then
      echo ">>> clone $repo"
      git clone -q "$url" "$dir" || failed+=("clone $url")
      continue
    fi

    if ! git -C "$dir" fetch -q --prune --tags --force origin 2>/dev/null; then
      echo ">>> fetch $repo 失败"; failed+=("fetch $url"); continue
    fi

    if [[ "$mode" == mirror ]]; then
      update_mirror "$dir" "$url" "$repo"
    else
      update_work "$dir" "$url" "$repo"
    fi
  done < "$list"
done < "$conf"

if [[ ${#failed[@]} -gt 0 ]]; then
  printf '\n失败 %d 个:\n' "${#failed[@]}" >&2
  printf '  %s\n' "${failed[@]}" >&2
  exit 1
fi
echo "全部成功"

