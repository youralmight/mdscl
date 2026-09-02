# DSCI 551 资源

来源只有一个：`resources/mds-2026-27/DSCI_551_stat-prob-dsci_students/`
网页版 https://pages.github.ubc.ca/mds-2026-27/DSCI_551_stat-prob-dsci_students/

Block 1 里材料做得最厚的一门：讲义、slides、可交互 demo、附录 cheatsheet 都有。但 **README 里一个 deadline 都没写**，全是 "Refer to the MDS calendar"。

## 读

| 是什么 | 在哪 |
|---|---|
| syllabus + 课程理念长文 + 6 条高层目标 | `README.md` |
| 8 讲讲义源（Quarto，R） | `notes/01..08_lecture-*.qmd` |
| 8 讲讲义渲染版 | `docs/notes/*.html` |
| 每讲学习目标 | `docs/learning-goals.html` / `website/learning-goals.qmd` |

**四份附录 cheatsheet**（`notes/appendix-*.qmd`）：
- `appendix-prob-cheatsheet` 概率
- `appendix-dist-cheatsheet` 分布
- `appendix-linear-algebra` 线代
- `appendix-greek-alphabet` 希腊字母

外链：Chris Piech *Probability for Computer Scientists*、Alex Tsun *Prob & Stat for CS*（PDF）、*Beyond Multiple Linear Regression*。

## 看

**没有视频，没有 pre-lecture video，也没有 pre-lecture quiz。**

有 8 套 slides：`slides/0N_lecture-*/` 每个目录下 `.qmd` 源 + `.html` 成品（reveal.js，浏览器直接开）。

## demo

两个可交互 HTML，在 `website/` 下，双击就能开：

- `probability-distributions-explained copy.html`（61 KB）— 分布交互演示
- `interactive_entropy_with_notes copy.html`（3.9 KB）— 熵

文件名带 " copy" 是没清理干净，不影响用。

## 跑

| 是什么 | 在哪 |
|---|---|
| 讲义 qmd 源（R 代码块） | `notes/*.qmd` |
| 生成讲义配图的独立 R 脚本 | `notes/supplementary/`（`expense.R`、`ggjointmarg.R`、`los_gang_joint.R`、`octane.R`、`ships.R`） |
| Quarto 站点工程 | `website/`（`_quarto.yml`、`website.Rproj`） |

要跑得装 R + Quarto。课程**明确推荐 RStudio + `.Rmd`**，理由是助教就是在这个环境开发和测试 lab 的，环境不一致他们没法帮你 debug。lab 要求交 **PDF**（从 Rmd 直接 render）。

## 练

学生版仓库里**没有** lab 题目。README 只列了四个 lab 的主题，deadline 全写 "Refer to the MDS calendar"。

| lab | 覆盖 |
|---|---|
| 1 | Depicting Uncertainty + Parametric Families（讲 1–2） |
| 2 | Joint and Conditional Probabilities（讲 3–4） |
| 3 | Continuous Distribution Families（讲 5–6） |
| 4 | MLE and Simulation（讲 7–8） |

## 备注

- **没有 worksheet，没有任何到场类分数**，100% 由 4 个 lab（各 12.5%）和 2 个 quiz（各 25%）决定。Block 1 四门课里唯一这样的。
- 全班教学评价回收率 ≥65% 的话，所有人 **+1% bonus**。
- 和 MDS-V 合班，001 = Payman Nickchi，002 = Alexi Rodríguez-Arelis。
- Slack 上问问题走 551 频道，不要私信；助教回复时间 9:00–17:00 周一到周五。
