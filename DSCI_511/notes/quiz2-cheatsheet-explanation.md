# DSCI 511 Quiz 2 Cheat Sheet：范围、来源与取舍

- 知识文档：[`quiz2-knowledge.md`](quiz2-knowledge.md)
- 考场内容稿：[`quiz2-cheatsheet.md`](quiz2-cheatsheet.md)

## 范围状态（2026-09-18）

**本学期尚无可在本地核验的 Quiz 2 逐项范围、练习题或专门 logistics。** 当前官方课程 README 只确认 Quiz 2 占总评 25%；`_quarto.yml` 预留了 Quiz 2 practice notebook 路径，却未把它作为已发布章节，且仓库中没有该 notebook。课程 `notes/messages.md` 没有 Quiz 2 公告。

因此，知识文档与本内容稿采用的**复习边界**是 Quiz 1 后已在本学期 `official/current/` 发布的 Pandas 主线：

1. Lecture 5：DataFrame 读入、检查、选择、向量化列运算、排序、过滤、缺失值、改名、删除与写出。
2. Lecture 6：tidy data、reshape、`concat`/`merge`、`apply`/`map`、`groupby`/`agg`。
3. Lecture 7：`Series.str`、时间对象与 `DatetimeIndex`、`resample`、`category`；regex 小节被讲义明确标为 OPTIONAL，未纳入。
4. 对应的已发布练习：Worksheet 5（Lecture 5 操作），Worksheet 6（filter、melt、pivot、reset index、map、groupby），及明示练习 Lectures 5–6 核心 Pandas 技能的 Lab 3。

不纳入：未发布的 Lecture 8（课程表写为 testing/generators，`_quarto.yml` 仍注释），`appendix_numpy.ipynb`、`appendix_plotting.ipynb`，以及未发布的 Quiz 2 practice questions。

- **[未确认]** Lecture 5–7 是否恰为 Quiz 2 的完整边界，是否存在排除主题，或 Quiz 1 的 Python/NumPy 基础是否会回考。
- **[未确认]** 本地当前来源没有把章节明确对应到教学周，也没有单独发布 Week 4 或 Quiz 2 说明；这里不把发布顺序冒充为教师公布范围。
- 这不是对考试内容的猜测或确认；教师公布范围后，应以其为准，按明确的纳入/排除项更新两个 Markdown 文件。

## 内容选择与压缩

- 保留：高频函数签名、返回类型/复制语义、按 label 与按位置的区别、`axis`、mask 运算符、reshape/merge 的选择规则、缺失值的含义、datetime/category 的关键访问器，以及容易静默得出错误结果的情形。
- 用小型表和最短可运行写法压缩：`pivot` 对比 `pivot_table`、`concat` 对比 `merge`、`apply` 对比 `map`、`loc` 对比 `iloc`。
- 删除：背景故事、数据集的具体答案、平台/截止日期、来源清单、课程政策、完整案例输出，以及虽在 Lecture 7 中出现但明确 OPTIONAL 的 regex 语法。
- 打印稿没有任何 LaTeX 数学 delimiter；公式/符号均使用普通文本、代码或 Unicode，以适配 `mdscl-cheatsheet` 的 Markdown/PDF/PNG 渲染器。

## 主要来源（均为本学期 `official/current/`）

1. `DSCI_511_py-prog_students/README.md`：课程学习目标、Lecture 5–8 主题、Quiz 2 权重。
2. `DSCI_511_py-prog_students/_quarto.yml`：已发布 Lecture 1–7、未发布 Lecture 8，以及未启用的 Quiz 2 practice chapter。
3. `DSCI_511_py-prog_students/lecture-notes/lecture5.ipynb`：DataFrame 操作。
4. `DSCI_511_py-prog_students/lecture-notes/lecture6.ipynb`：reshape、组合、函数应用、分组聚合。
5. `DSCI_511_py-prog_students/lecture-notes/lecture7.ipynb`：字符串、datetime、categorical；regex OPTIONAL 状态。
6. `DSCI_511_py-prog_students/worksheets/worksheet5/student/worksheet5.ipynb` 与 `worksheets/worksheet6/student/worksheet6.ipynb`：已发布练习覆盖。
7. `DSCI_511_py-prog_students/labs/lab3/student/lab3.ipynb`：明示练习 Lectures 5–6 核心 Pandas 技能。
8. `DSCI_511/notes/messages.md`：无 Quiz 2 公告的本地课程消息记录。
