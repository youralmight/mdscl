# DSCI 523 Quiz 2 Cheat Sheet — Companion Explanation

**不进入考场。**本文件保存不应放入考试用 [Cheat Sheet](quiz2-cheatsheet.md) 的范围、来源和压缩决定；完整解释见 [Quiz 2 知识复习](quiz2-knowledge.md)。

## 范围证据与不确定性

- 当前学年 `official/current/DSCI_523_r-prog_students/README.md` 明确 Quiz 2 占总评 **30%**、window 为 **2026-09-29–10-02**，但没有明示 lecture 范围、题型、资源许可或 practice quiz。
- 本地 current tree 没有单独 Quiz 2 公告或 scope sheet。Quiz 1 后已发布、与下一阶段直接相关的材料是 Lecture 5–6 讲义、Lecture 5 section-001 skeleton、Worksheet 5–6、Lab 3 和 section-002 的 Lecture 5–6 examples。因此知识稿和 Cheat Sheet 以 **Lecture 5–6 的已发布非 optional 内容**为可审计的复习边界。
- **[未确认]** Lecture 7–8 是否被纳入 Quiz 2：07/08 lecture notebooks 虽已存在于 current tree，但本地没有把它们列为 Quiz 2 的教师说明，也没有相应已发布的 Worksheet 7–8 / Lab 4 练习作为本次范围证据。它们未进入知识稿或 Cheat Sheet；教师后续公告应优先于此边界。
- `...` 的手动处理在 Lecture 6 标为 Optional – Advanced；Worksheet 5 的 5–6 题、Worksheet 6 的 2/4/5 题和 Lab 3 的 5–6 题也明确为 optional/challenging/未计分。Cheat Sheet 仅保留理解 `map*` 传参所必需的一行提醒，不把这些扩展练习作为已确认考点。
- 只用当前学年 `official/current/` 材料；没有以 `official/public/` 历史课程替代未发布范围。

## Cheat Sheet 的内容选择与压缩

Cheat Sheet 留下会决定代码结果或输出形状的规则：

- `case_when()` 默认分支、factor 转 character、`is.na()`、按列或全表的 `drop_na()`；
- `group_by()`、`summarise()` 和 grouped `mutate()` 的行数差异、`n()`、`na.rm` 和 `ungroup()`；
- `map`/`map_*` 的返回形状、类型后缀和 `...` 传参；
- 函数定义、默认值、最后表达式返回、惰性求值与作用域；
- `testthat` expectation 选择、TDD、`stop()`/`warning()`/`try()`；
- roxygen2 contract、`source()`、样本方差和提交前的形状检查。

删除了课程日期、权重、范围状态、作业平台说明、练习 rubric、完整背景解释、来源清单和重复示例。这会使条目密集；需要判断“为什么”或补看 `case_when`、分组状态、作用域与 TDD 的完整上下文时，应回到知识稿。

## 打印与渲染约束

Cheat Sheet 只使用纯文本、代码和 Unicode，不含 `$...$`、`$$...$$`、`\(...\)`、`\[...\]` 等 LaTeX 数学分隔符，以兼容本地 `mdscl-cheatsheet` 渲染器。渲染产物与 Markdown 并列保存：HTML 供浏览器检查，PDF 用于打印，PNG 为每个 PDF 页面提供快速预览。

## 当前学年来源

- `official/current/DSCI_523_r-prog_students/README.md` 与 `lec_learning_objectives.md`。
- `jupyter-book/lecture-notes/05-tidy-control-flow.ipynb`、`06-lecture-functions-and-testing.ipynb`。
- `section-001/lecture-5-skeleton-pre.ipynb`。
- `section-002/lecture5-example-problems.md`、`lecture6-example-problems.Rmd`。
- `release/worksheet5/worksheet5.Rmd`、`release/worksheet6/worksheet6.Rmd`、`release/lab3/lab3.Rmd`。
- `DSCI_523/notes/resources.md`、`DSCI_523/notes/messages.md`：未记录额外的 Quiz 2 scope 公告。
