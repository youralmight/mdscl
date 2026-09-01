# 来源清单

记位置，不记内容。内容会变，位置不太会。

## Canvas

https://canvas.ubc.ca/

25 门课，目前只有 2 门能进（DSCI_V 523、项目 hub "MDS-CL 2026-2027"），其余 unpublished。

- 学期节奏（Block / quiz week / 假期 / 调课）→ hub 的 Calendar
- 评分权重 → 各课 Grades 页
- office hour、老师 TA 名单、career 资源、项目邮箱 → hub
- **拿不到**：常规上课时间和教室、syllabus、权威 deadline 列表、老师邮箱

Canvas 是跳板不是信息中心，课程内容都外链到 github.ubc.ca。

## GitHub Enterprise（MDS-2026-27）— 学生版，权威

https://github.ubc.ca/MDS-2026-27

**这学期实际在用的东西都在这里。** 只有 5 个 repo（只 share 已开课的）：

| repo | 内容 |
|---|---|
| `DSCI_523_r-prog_students` | 完整 syllabus（8 讲安排、每讲 required readings/videos、全部 deadline、政策）+ 8 讲讲义 notebook + HTML 版 |
| `DSCI_551_stat-prob-dsci_students` | syllabus（纯 assignment-based 评分）+ slides + lab 评分算法 |
| `lab-sections` | 全项目 191 人的分组名单 CSV（lab L01–L04 × lecture 1–2 × CL 标记） |
| `orientation` | orientation 的 5 个 PDF（slides、faculty、study habits、health） |
| `student-reps` | 学生代表 |

访问要 token，凭据存在 `~/.git-credentials`（仓库外）。

本地副本：`resources/mds-2026-27/`（gitignore），名单 `mds-2026-27.txt`。

## GitHub org（UBC-MDS）— 教材公开版，往年

https://github.com/UBC-MDS

76 个 public repo，其中 **26 个是课程 repo**（`DSCI_*` 前缀）。**没有任何 `COLX_*`**——CL 专属课程在公开 org 上完全没有。

价值和坑：

- **能拿到往年的 lab / worksheet 原件**：如 `DSCI_551_stat-prob-dsci/release/lab1..lab4/`（含 autograder tests）、`DSCI_523_r-prog/worksheets/1..8`。这是最好的练手材料。
- **能拿到其他课的 syllabus**，包括 511、512、573、575 等还没 share 的课。
- ⚠️ **评分方案会逐年变，尤其是出勤相关项**。已验证：523 老版没有 pre-lecture quiz，新版加了 4%；551 老版有 2% iClicker 出勤，新版删了。**老 syllabus 只能参考，不能当准。**
- `DSCI_521_platforms-dsci` 是空的（README 只有一行）。

本地副本：`resources/ubc-mds/`（gitignore），名单 `ubc-mds.txt`。

同步（两个都管）：仓库根的 `./sync_course_repos.sh`，没有就 clone，有就 pull。

## MDS-CL 项目站

https://ubc-mdscl.github.io/

项目介绍、课程概览、政策、Career、Capstone。

Calendar 页指向 https://ling.air.arts.ubc.ca/mds-cl-calendar/ ——**要 UBC 登录，浏览器 session 也进不去**，没验证过里面有什么。

另有一个 https://ubc-mds.github.io/calendar/ ，523 和 551 的 syllabus 都指向它当作课表权威源。**未查。**

## UBC 项目官网

https://masterdatascience.ubc.ca/programs/computational-linguistics

未查。

## Slack

未查。不好自动化访问，大概率要手动。

## 邮件 / Welcome Package（桌面）

`~/Desktop/orrientationrelatedemails/`

**目前信息密度最高的一份**：`2026_MDS_CL_Welcome_Package final (1).pdf` 第 10 页有**全年课表**（每门课、活动类型、星期、时长、日期区间、是否 MDS-CL ONLY）。

已确认：Block 1 = 2026-08-31 → 2026-10-01（5 周），Block 2 = 2026-10-05 → 2026-11-05。
