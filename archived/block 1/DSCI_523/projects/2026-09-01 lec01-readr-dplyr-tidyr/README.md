# 2026-09-01 DSCI 523 lec01 — readr / dplyr / tidyr

覆盖 523 第一讲全部 learning objectives 的可执行 demo。

```
lec01-demo.ipynb   主文件。92 个 cell，57 个是代码
make-data.R        生成 data/ 下的数据文件
command.sh         命令行验证
data/              数据（由 make-data.R 生成）
```

## 覆盖的 objectives

| objective | 在第几节 |
|---|---|
| 用 `<-` 赋值 | 1 |
| `readr::read_csv` 读标准 csv | 2 |
| 选对 `read_*` 函数和参数，读进不规整的纯文本 | 3 |
| `readr::write_csv` 写出 | 4 |
| `select` `filter` `mutate` `arrange` `desc` `slice` `pull` `%in%` | 5 |
| 管道 `\|>` | 6 |
| tidy data 的定义 | 7 |
| tidy 格式的优点和缺点 | 7 |
| `tidyr::pivot_wider` / `pivot_longer` | 8 |

第 9 节是四道综合练习，答案在后面（先自己写）。最后有速查表。

## 数据

来自 **`gapminder` 包**（真实数据，不是编的），取 5 个国家 × 12 年 = 60 行，
由 `make-data.R` 写成六种格式，专门用来练 `read_*` 的参数：

| 文件 | 特点 | 练什么 |
|---|---|---|
| `gapminder.csv` | 干净 | `read_csv` |
| `gapminder.tsv` | 制表符 | `read_tsv` |
| `gapminder-semicolon.txt` | 分号 | `read_delim(delim = ";")` |
| `gapminder-messy.csv` | **4 行注释 + 没表头 + 缺失值写成 `N/A` 和 `-99`** | `comment` `skip` `col_names` `na` |
| `life-expectancy-wide.csv` | 12 个年份摊成 12 列 | `pivot_longer` |
| `measurements-long.csv` | 三个变量叠在一列 | `pivot_wider` |

`canada.csv` 和 `low-life-exp.csv` 是跑 notebook 时写出来的，删了会自动重建。

## 怎么用

```bash
codium "/Users/youralmight/workspaces/reps/mdscl/DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr"
```

打开 `lec01-demo.ipynb` → 右上角 kernel 选 **R 4.6.1** → 从头 `⇧Enter` 按到底。

每节末尾有「动手」小题，第 9 节有四道综合题——那几个 cell 是空的，自己填。

## 已验证

整个 notebook 无头跑过：**57 个代码 cell，0 报错**。抽查了关键输出：

- 反面教材那个 cell 确实读成了一团糟（63 行 × **1 列**，列名变成 `# Gapminder extract`）
- ggplot 那张折线图渲染出了 105 KB 的 PNG
- `pivot_longer` → `pivot_wider` 转回来，`all.equal` 返回 `TRUE`
- Q4 写出的文件内容正确

所以跑不通就是自己改坏了。
