# DSCI 551 Quiz 2 Cheat Sheet Explanation

> **不进入考场。** 本说明保存 [Quiz 2 knowledge document](quiz2-knowledge.md) 与考试用 [Cheat Sheet](quiz2-cheatsheet.md) 之间的范围证据、来源和压缩取舍。用户已授权当前创建知识稿和考试稿；Cheat Sheet 的内容选择严格限于当前已发布的本地材料。

## 范围与评估状态

- **[未确认] Quiz 2 的正式范围。** 当前本地 DSCI 551 checkout 没有 `Quiz 2`、`quiz2` 或等价明确范围说明；`notes/messages.md` 没有后续 assessment announcement；课程 README 仅列 Quiz 1、Quiz 2 各占 25%，并让学生参考 MDS calendar。
- 为避免凭课程顺序猜测，知识稿和 Cheat Sheet 的可审计工作边界是：Lecture 5 和 6 的 learning goals，以及与其对应、已发布的 Lab 3。课程 README 将 Lab 3 标为 Continuous Distribution Families (Lectures 5 and 6)；Lab 3 开头明确列出连续/离散模型、PDF、CDF、quantile、prediction interval、连续分布族、二元密度、条件密度和连续变换。
- Lecture 7–8 的材料已存在于当前仓库，但没有将其纳入 Quiz 2 的明确证据，因此没有把 MLE 或 simulation 放入考试稿。若之后发布的 Quiz 2 instruction 明示涵盖它们，应重新扩充，而不是把本稿当作完整范围。
- 题数、题型、日期/时间窗、ORCA reservation、评分/partial credit 和允许资源（个人 Cheat Sheet、计算器、RStudio、网络、文件等）均为 `[未确认]`。评估资源和行为规则必须以 Quiz/ORCA 的 assessment-specific instructions 为准；这些行政内容未放入 Cheat Sheet。

## 当前本地来源

1. `official/current/DSCI_551_stat-prob-dsci_students/website/learning-goals.qmd`：Lecture 5–6 的 learning goals；并显示 Lecture 7–8 的不同主题。
2. `official/current/DSCI_551_stat-prob-dsci_students/notes/05_lecture-continuous.qmd`：连续变量、PDF、连续摘要、median/quantile/prediction interval、skewness、CDF、survival 与 quantile function。
3. `official/current/DSCI_551_stat-prob-dsci_students/notes/06_lecture-continuous-families.qmd`：七个连续分布族、R 的 d/p/q/r、二元 PDF、区域概率及连续条件分布。
4. `official/current/DSCI_551_stat-prob-dsci_students/release/lab3/student/lab3.Rmd`：当前已发布 Lab 3 的具体应用与判断规则，尤其是 family selection、continuous/discrete comparison、二元 Uniform、valid CDF、条件密度和 `Y=X²` 变换。
5. `official/current/DSCI_551_stat-prob-dsci_students/README.md`：Lecture/lab map、Lab 3 与 Lecture 5–6 的关联、Quiz 权重与仅指向 calendar 的 Quiz 信息。
6. `notes/resources.md` 与 `notes/messages.md`：确认当前本地无 worksheet，且没有额外 Quiz 2 scope announcement。

未使用 `official/public/`；它是历史材料，不能代替本学期要求。

## 内容选择与压缩

Cheat Sheet 保留可直接完成已发布连续概率题的内容：PDF/CDF/survival/quantile 的转换；连续分布的均值、方差、分位数、预测区间；连续分布族的过程选择、支持、参数、公式和 R 调用；二元区域概率、边缘与独立；条件密度；以及连续变换的 CDF-first 方法。

为压缩而保留的高风险提醒包括：连续单点概率为 0；PDF 高度不是概率；CDF 的四个合法性条件；Normal 的 `sd` 与方差不同；Exponential 在 R 中使用 `rate`；正值或右偏不足以辨认家族；连续变换必须加入尺度导数；联合 PDF 只有在独立时才分解；条件密度需要限制支持并归一化。

以下内容有意不放进考试稿：范围/日期/平台/诚信和来源信息；长篇直觉叙述；完整 Gamma-function 推导；Lab 3 的题号、提交格式与 rubric；以及没有范围证据的 Lecture 7–8。知识稿保留这些边界和更完整的解释，供考试稿之外的复习与审核使用。

Cheat Sheet 只使用纯文本与 Unicode 数学记号，没有 `$...$`、`$$...$$`、`\(...\)` 或 `\[...\]` 等 LaTeX 数学分隔符，以兼容本地 `mdscl-cheatsheet` 渲染器。
