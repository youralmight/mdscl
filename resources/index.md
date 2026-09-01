# 来源清单

记位置，不记内容。内容会变，位置不太会。

具体内容归 `my_notes/`。这里出现的每一行都该是"去哪找"，不是"里面写了什么"。

分两部分：**通用**是每门课都适用的渠道；**按课**只记那些不走通用规则的课。

## Canvas

https://canvas.ubc.ca/

跳板，不是信息中心。只有已开课的能进。

- 学期节奏（Block / quiz week / 假期 / 调课）→ 项目 hub "MDS-CL 2026-2027" 的 Calendar
- 评分权重 → 各课 Grades 页
- office hour、老师 TA 名单、career 资源、项目邮箱 → hub
- **课程材料的外链** → 各课页面。⚠️ 有的课只在这里给一个外链，别处再无指路，见「按课」
- **拿不到**：上课时间和教室、权威 deadline 列表、老师邮箱

## GitHub Enterprise（MDS-2026-27）— 学生版，权威

https://github.ubc.ca/MDS-2026-27

本学期实际在用的材料，只 share 已开课的。

要 token，凭据在 `~/.git-credentials`（仓库外）。本地副本 `resources/mds-2026-27/`（gitignore）。

## GitHub org（UBC-MDS）— 教材公开版

https://github.com/UBC-MDS

往年课程材料，`DSCI_*` 前缀，**没有 `COLX_*`**。往年 lab / worksheet 原件是最好的练手材料。

⚠️ 两个坑：评分方案逐年变，老 syllabus 只能参考；**这里有 repo 是本学期的**，别当往年看。

本地副本 `resources/ubc-mds/`（gitignore）。同步 `./sync_course_repos.sh`，来源配置在仓库根 `sources.conf`。

## MDS-CL 项目站

https://ubc-mdscl.github.io/

项目介绍、课程概览、政策、Career、Capstone。

Calendar 页指向 https://ling.air.arts.ubc.ca/mds-cl-calendar/ ——**要 UBC 登录，浏览器 session 也进不去**，未验证。

另有 https://ubc-mds.github.io/calendar/ ，523 和 551 的 syllabus 都拿它当课表权威源。**未查。**

## UBC 项目官网

https://masterdatascience.ubc.ca/programs/computational-linguistics

未查。

## Slack

未查。不好自动化访问，大概率要手动。

## 邮件 / Welcome Package（桌面）

`~/Desktop/orrientationrelatedemails/`

`2026_MDS_CL_Welcome_Package final (1).pdf` 第 10–13 页是全年课表，已抄进 `my_notes/courses/index.md`。


