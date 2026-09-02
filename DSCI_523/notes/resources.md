# DSCI 523 资源

`../official/current/DSCI_523_r-prog_students/`
网页版 https://pages.github.ubc.ca/MDS-2026-27/DSCI_523_r-prog_students/README.html

按"我拿它干什么"分类。路径都相对仓库根。

---

## ① 搞清楚规则 —— 开学看一次就够

```
README.md                      15 条学习目标、8 讲主题、完整 deadline 表、
                               pre-lecture quiz 规则、师资、评分权重
lec_learning_objectives.md     每讲拆细的学习目标
```

**Block 1 唯一一门 deadline 白纸黑字写死的课**，不用查日历：

| | 时间（PT） |
|---|---|
| Lab 1 / 2 / 3 / 4 | 09-05 18:00 / 09-13 **12:00** / 09-20 **12:00** / 09-26 18:00 |
| Worksheet 1–8 | 09-06、09-06、09-13、09-13、09-20、09-20(**11:59**)、09-27、09-27 |
| Quiz 1 / 2 | 09-15→09-18 / 09-29→10-02 |

Lab 2、3 是中午 12 点。Worksheet 6 是 11:59。其余 18:00。

---

## ② 课前 —— 有分数挂钩，跑不掉

**看视频**：8 讲每讲都有，README 里那列的表头就叫 `Required videos`。仓库里没有文件，是外链。

⚠️ 链接指向 `canvas.ubc.ca/courses/192993/...`，**192993 是往年课号**，今年入口要自己在 Canvas 找。

**为什么跑不掉**：每讲开头 15 分钟纸质闭卷小测，考的就是视频内容，全学期 4%，缺席 0 分，无补考。

**读**（外链，仓库内无副本，8 讲里 6 讲有）：*Introduction to Data Science*（UBC 自己写的）、STAT 545、*R for Data Science*、*Advanced R*、*Programming with dplyr*。

---

## ③ 上课 —— 老师 demo + 小组做 worksheet

课堂流程（README 原话）：老师按视频内容现场演示，然后分小组做一个 worksheet notebook。课会录播。

讲义 8 讲全齐，两种形态：

```
读（不用装 R，浏览器开）
  docs/lecture-notes/*.html        01 intro-to-r-via-tidyverse
                                   02 data-types-and-operators
                                   03 dates-strings-and-factors
                                   04 two-table-joins-and-base-control-flow
                                   05 tidy-control-flow
                                   06 functions-and-testing
                                   07 mapping-and-nested-data-frames
                                   08 tidy-evaluation

跑（要 R + IRkernel）
  jupyter-book/lecture-notes/01..08-*.ipynb    同样 8 讲，可执行
```

**worksheet 的题目仓库里没有**，上课当场发。

---

## ④ 自己动手 —— 讲义配套的可跑材料

```
jupyter-book/lecture-notes/
├── data/            同一份加拿大语言普查数据的 6 种格式：
│                    can_lang .csv / .tsv / .xlsx / .db(sqlite)
│                    + can_lang-colnames.csv / -meta-data.csv / can_lang7.csv
│        x            + census_snippet.csv
│                    ← 就是专门用来练"读各种鬼格式文件"的
├── src/kelvin_to_celsius.R    讲义里 source() 进去的示例函数
└── temp.xlsx                  讲义里写文件产生的输出样例
```

除此之外**没有练习题**：没有 lab 题、没有 worksheet 题、没有 quiz 练习题。

---

## ⑤ 不用管

```
docs/_sources/  docs/_static/  docs/_images/  jupyter-book/_build/
jupyter-book/README.md          构建时从顶层拷来的副本
Makefile                        `make book` 的构建脚本
_config.yml  _toc.yml
```

`docs/` 整个是构建产物，改了会被覆盖。只当网页版读，别编辑。

---

## ⑥ 平台

README 里没给 Canvas / Gradescope 链接（511 给了，523 没给）。课表和 office hour 指向 https://ubc-mds.github.io/calendar/ ——**这是 MDS-V 的日历，CL 的在 https://ling.air.arts.ubc.ca/mds-cl-calendar/**。

---

## 备注

README 版权 © 2021 Tiffany Timbers，讲义主体沿用多年。001 = Gittu George，002 = Tiffany Timbers（也是 lab instructor）。
