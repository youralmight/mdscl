# 2026-08-31 DSCI 523 self-learning-demo

一次性的隔离工作目录。目的：**把 R 工具链的三种运行方式各跑通一遍**，
确认环境是好的，也熟悉编辑器里该按哪些键。

不是课程材料的副本——全是为了演示而写的最小例子。

## 三个文件夹 = 三种运行场景

| | 文件 | 对应什么 |
|---|---|---|
| `1-r-script/` | `demo.R` | 平时写脚本、调代码。逐行 ⌘Enter 送进 R 终端 |
| `2-notebook/` | `demo.ipynb` | **DSCI 523 的 8 讲讲义就是这种**。R kernel |
| `3-rmarkdown/` | `demo.Rmd` | **DSCI 551 交 lab 走这条路**，最后要出 PDF |

每个文件开头都有注释写清楚该按什么键、这个 demo 在演示什么。
按顺序 1 → 2 → 3 走一遍即可。

## 怎么开始

先在编辑器里打开这个目录：

```bash
cursor "/Users/youralmight/workspaces/reps/mdscl/project/2026-08-31 DSCI 523 self-learning-demo"
```

（或者 `./command.sh open`）

然后：

1. 打开 `1-r-script/demo.R`，光标放第一行，**⌘Enter** 一路按到底
2. 打开 `2-notebook/demo.ipynb`，右上角 kernel 选 **R 4.6.1**，**⇧Enter** 一路按到底
3. 打开 `3-rmarkdown/demo.Rmd`，**⇧⌘Enter** 逐块跑，最后 **⇧⌘K** 出 PDF

## command.sh —— 命令行等价物

一行一条命令，打开自己复制着跑；也可以 `bash command.sh` 整个跑一遍。

用处是**区分是操作问题还是环境问题**：
命令行通、编辑器不通 → 编辑器配置问题（多半是没重启）。
命令行也不通 → 环境问题。

## 已验证

| 场景 | 结果 |
|---|---|
| 1 `.R` | `Rscript demo.R` 退出码 0，无报错 |
| 2 `.ipynb` | 7 个代码 cell，**1 个报错——是 demo 里故意写错的那个**，其余全过 |
| 3 `.Rmd` | 生成 `3-rmarkdown/demo.pdf`，260 KB |

## 写这几个 demo 时踩到的两个坑（都写进文件注释里了）

1. **`.Rmd` 里，HTML 注释中的行内 R 代码照样会被执行。**
   我在注释里想解释行内代码的语法，直接写了那个语法，knit 就报
   `'...' used in an incorrect context`，整个渲染失败。

2. **命令行跑 `.R` 时，`ggplot` 的图会被默默存成 `Rplots.pdf`。**
   没有面板可显示。所以 `./command.sh 1` 只能证明代码没写错，
   证明不了绘图面板配好了——那个必须在编辑器里看。

## 注意

`3-rmarkdown/demo.pdf` 是构建产物，删了随时能重新生成。
