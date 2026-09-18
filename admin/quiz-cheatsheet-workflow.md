# Quiz 知识文档与 Cheat Sheet 工作说明

## 要做什么

先为每门 Quiz 写一份完整、简洁、真正适合复习的 Markdown 知识文档。此时不要猜用户已经会什么，也不要急着压缩成一页。

知识文档完成后，用户会分别和三个课程 Agent 沟通，选择哪些内容进入 Cheat Sheet。考试时使用的 Markdown 与范围、来源和取舍说明分开保存；图片和页面排版最后再决定。

## 公式写法（硬约束，先读这一节）

这两个文档的消费者都没有数学引擎：`mdscl-cheatsheet`（Python-Markdown + WeasyPrint → Letter PDF/PNG）和 GitHub / Obsidian 的 Markdown 预览。规则按文档分两种：

- **`quiz1-cheatsheet.md`（要打印）不能出现任何 LaTeX 数学标记。** `$...$`、`$$...$$`、`\(...\)`、`\[...\]` 都不要：渲染器会把 `$P(A)$` 原样打进 PDF/PNG；`\(S\)` 还会被吃掉反斜杠变成 `(S)`，`\cap` 直接打印成 `\cap`。公式写成纯文本 / Unicode，例如 `P(Aᶜ) = 1 − P(A)`、`P(A | B) = P(A ∩ B) / P(B)`、`Var(X) = E[X²] − E[X]²`、`Σᵢ P(A | Bᵢ)P(Bᵢ)`、`X ∼ Bernoulli(p)`、`(1 − p)/p²`。渲染器会直接报错拦住 LaTeX 输入，不会静默产出坏图；R/Python 代码里的 `$`（`df$mass`）写在 code span 里，不受影响。
- **`quiz1-knowledge.md`（只阅读、不打印）可以用 `$...$` / `$$...$$`**，GitHub、Obsidian、VS Code 都能渲染。但**不要把 display 公式缩进进列表项**：GitHub 不渲染缩进在列表里的 `$$` 块，会原样显示 `$$`。要 display 就把 `$$` 放第 0 列，否则把它写成行内公式放进列表项那一行。

## 当前分工

| 课程 / Quiz | 第一阶段文件 | 考试用内容 | 说明文件 |
|---|---|---|---|
| DSCI 511 — Quiz 1 | `DSCI_511/notes/quiz1-knowledge.md` | `DSCI_511/notes/quiz1-cheatsheet.md` | `DSCI_511/notes/quiz1-cheatsheet-explanation.md` |
| DSCI 511 — Quiz 2 | `DSCI_511/notes/quiz2-knowledge.md` | `DSCI_511/notes/quiz2-cheatsheet.md` | `DSCI_511/notes/quiz2-cheatsheet-explanation.md` |
| DSCI 523 — Quiz 1 | `DSCI_523/notes/quiz1-knowledge.md` | `DSCI_523/notes/quiz1-cheatsheet.md` | `DSCI_523/notes/quiz1-cheatsheet-explanation.md` |
| DSCI 523 — Quiz 2 | `DSCI_523/notes/quiz2-knowledge.md` | `DSCI_523/notes/quiz2-cheatsheet.md` | `DSCI_523/notes/quiz2-cheatsheet-explanation.md` |
| DSCI 551 — Quiz 1 | `DSCI_551/notes/quiz1-knowledge.md` | `DSCI_551/notes/quiz1-cheatsheet.md` | `DSCI_551/notes/quiz1-cheatsheet-explanation.md` |
| DSCI 551 — Quiz 2 | `DSCI_551/notes/quiz2-knowledge.md` | `DSCI_551/notes/quiz2-cheatsheet.md` | `DSCI_551/notes/quiz2-cheatsheet-explanation.md` |

每个 Agent 只负责自己的一门课。DSCI 521 没有正式 Quiz，不在这里。`official/` 只读，成品写入相应课程的 `notes/`。

## 第一阶段：写完整知识文档

先阅读本学期与该 Quiz 有关的材料，包括教师公布的考试范围、learning objectives、lecture notes、slides、practice quiz、worksheet、lab 和课程通知。

优先相信本学期教师的明确说明和 `official/current/`。历史公开材料只能辅助理解，不能用来替代本学期要求。来源冲突或范围无法确认时，清楚写出 `[未确认]`，不要猜。

最终文档应该让学生能够用它理解和复习本次 Quiz 的全部可考知识，而不是一份讲义目录或材料摘要。

写作要求：

- 完整覆盖已经明确的考试范围和 learning objectives。
- 按概念之间的关系组织内容，不必机械照搬 lecture 或文件顺序。
- 概念要解释到能用；公式要说明符号、适用条件和判断方法。
- R/Python 函数写清用途、关键参数、返回结果和容易出错的地方。
- 例子只在有助于理解时加入，并使用能说明问题的最小例子。
- 容易混淆的概念用对比表、判断规则或正反例讲清楚。
- 不复制整段讲义，不堆叠重复例子，不加入与考试无关的背景。
- 不因为 Agent 觉得某项“太基础”或猜测用户已经掌握，就省略可考内容。
- 来源在相关章节末尾或文档末尾简单列出即可，不要给每句话做繁琐标注。

“简洁”是减少重复和废话，不是减少知识；“完整”是覆盖可考内容，不是复述所有课堂文字。

写完后自己对照考试范围和 learning objectives 查漏，修正明显重复、错误和矛盾。然后把文件路径、已覆盖范围以及仍未确认的事项告诉用户。

第一阶段到这里停止：不要自动生成 Cheat Sheet，不要开始排版，也不要生成图片。

## 第二阶段：用户选择 Cheat Sheet 内容

只有用户开始选择后，才创建对应的 `quiz1-cheatsheet.md` 与 `quiz1-cheatsheet-explanation.md`。

用户决定哪些内容加入、删除、展开或压缩。Agent 可以指出遗漏、依赖关系和空间代价，也可以提出建议，但不能根据自己的判断替用户决定“这个不用记”。

`quiz1-cheatsheet.md` 是考试时实际使用、未来转成图片的内容稿，只保留公式、代码模板、对比、例子、判断规则和易错提醒。不要放考试范围、日期、分值、地点、平台操作、来源、审查记录、诚信说明或文档使用说明。

`quiz1-cheatsheet-explanation.md` 不进入考场，用于保存上述范围与来源信息，并简要记录内容选择和压缩取舍。它应链接知识文档与考试用内容稿。

此时仍不需要决定具体排版工具。等内容基本确认后，再处理 Letter 单面页面、至少 8 pt、填满可用空间、打印可读以及 PNG 不超过 5 MB 等要求。

Quiz 2 可以沿用同样流程，文件名中的 `quiz1` 改为 `quiz2`。
