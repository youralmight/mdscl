# DSCI 511 资源

`resources/mds-2026-27/DSCI_511_py-prog_students/`
网页版 https://pages.github.ubc.ca/mds-2026-27/DSCI_511_py-prog_students/

Quarto **book** 工程。整个仓库 77 个文件，结构最扁平的一门。

## 文件结构

```
DSCI_511_py-prog_students/
├── README.md              📄 syllabus——8 讲主题表、readings、评分表、
│                             口试(oral check-in)规则、师资、四个平台链接
├── index.qmd              📄 Quarto book 首页（内容就是 README）
├── _quarto.yml            ⚙️ 目录配置。⚠️ 注释掉的部分泄露了后续计划，见下
├── style.css              ⚙️
├── pyproject.toml         🔧 环境：uv 项目
├── uv.lock                🔧    锁定版本，可 `uv sync` 一比一复现助教的环境
├── .python-version        🔧
└── lecture-notes/
    ├── lecture1.ipynb     📘 讲义正文（Python）
    ├── lecture2.ipynb     📘
    ├── lecture3.ipynb     📘
    ├── lecture4.ipynb     📘   ← 到此为止，5–8 讲未放
    ├── lec1_script.py     ▶️ 第 1 讲配套的独立脚本（讲"怎么跑 .py 文件"用的）
    ├── code/
    │   └── bad_style.py   ▶️ 代码风格反面教材，讲 PEP8 时现场改
    ├── data/              📊 20 个：titanic / imdb / cycling_data / YVR_weather /
    │                         Olympics_2024 / WACL / bean / sales / student_scores /
    │                         weather1-4 / measurements.tsv / likes_dislikes.tsv /
    │                         villains.txt / hello.py / World_Development_Indicators.xlsx
    └── img/               🖼 42 个插图，含 5 个 gif（pandas_stacking、melt_pivot、
                              convolution、computer_panda）
```

图例：📄 说明 / 📘 讲义正文 / ▶️ 可跑的演示 / 📊 数据 / 🖼 素材 / ⚙️ 站点配置 / 🔧 环境

## `_quarto.yml` 里注释掉的东西

这是唯一能提前知道后面会发什么的地方。文件里被注释掉、但明显是排好版的章节：

```
# lectures/notes/00_course-information.ipynb        ← "Getting ready"
# lecture-notes/lecture5.ipynb ~ lecture8.ipynb     ← 剩下 4 讲
# lectures/slides/lecture_01.qmd                    ← "Lecture Slides"（现在一套都没有）
# quiz1_details.qmd                                 ← "Quiz Logistics"
# quiz1-practice-questions/quiz1-practice-questions.ipynb
# quiz_practice_questions/quiz1/... quiz2/...       ← 两次 quiz 的练习题
# lectures/demos/transformers-recipe-generation.ipynb  ← "Class demos"
# lectures/notes/AppendixA-text-preprocessing.ipynb
# lectures/notes/AppendixB-BaumWelch.ipynb          ← "Appendices"
```

**会有 quiz 练习题**，两次各一份。附录是文本预处理和 Baum-Welch（HMM），class demo 是 transformer 做菜谱生成——这几项是 CL 版特有的，MDS-V 的 511 不会有。

## 仓库里没有的

- **worksheet 和 lab 的题目**：一个都没有。
- **slides**：一套都没有（`_quarto.yml` 里那栏是空的注释）。
- **视频**：仓库里没有。README 的 lecture 5/6/7 行挂了 YouTube 链接（"Programming in Python for Data Science" 系列，带时间戳），但那一列的表头是 **Supplemental videos**——补充，不是课程要求。511 没有 pre-lecture video 机制。

## 外部平台

| | |
|---|---|
| Canvas | https://canvas.ubc.ca/courses/193140 |
| Gradescope | https://www.gradescope.ca/courses/39186 |
| **PrairieLearn** | https://us.prairielearn.com/pl/course_instance/219073 |
| 日历（CL） | https://ling.air.arts.ubc.ca/mds-cl-calendar/ |

PrairieLearn 只有 511 提，Block 1 另外三门都没有。用途未知。

## 外链教材（仓库内无副本）

Runestone *Foundations of Python Programming*、*Python Data Science Handbook*、*A Whirlwind Tour of Python*、*Data Science: A First Introduction with Python*、*Think Python*、Wes McKinney *Python for Data Analysis*、Kaggle Learn、numpy/pandas 官方文档。全部免费在线。
