#!/usr/bin/env bash
# 一行一条命令，从上往下自己复制着跑。也可以 bash command.sh 整个跑一遍。
cd "$(dirname "${BASH_SOURCE[0]}")"


# ---- 环境自检 ----

R --version | head -1

Rscript -e 'cat(rownames(installed.packages()), sep="\n")' | grep -xE 'tidyverse|IRkernel|httpgd|languageserver|rmarkdown|knitr|tinytex|ottr|testthat|digest'

Rscript -e 'cat("LaTeX:", tinytex::is_tinytex(), "\n")'

cat ~/Library/Jupyter/kernels/ir/kernel.json

cursor --list-extensions | grep -iE 'reditor|r-debugger|quarto|jupyter'


# ---- 场景 1：.R 脚本 ----
# 编辑器里：光标放某行，⌘Enter。命令行等价物 = ⇧⌘S（Run Source）。
# 注意：图没有面板可显示，会被存成 Rplots.pdf。绘图面板必须在编辑器里看。

Rscript 1-r-script/demo.R

rm -f Rplots.pdf


# ---- 场景 2：.ipynb（R kernel）----
# 编辑器里：右上角 kernel 选 R 4.6.1，然后 ⇧Enter 一路按到底。
#
# --execute 才是干活的那个：起 kernel，从上到下跑完所有 cell，把输出写回去。
# --to notebook 只是说"输出还是 notebook"（不加的话默认转 HTML）。
# --allow-errors 让它遇错不停 —— demo 里有一个故意写错的 cell。
#   但加了它退出码永远是 0，所以下一行自己数报错个数，应该正好 1 个。

uvx --from nbconvert jupyter nbconvert --to notebook --execute --allow-errors --output /tmp/demo_run.ipynb 2-notebook/demo.ipynb

grep -c '"output_type": "error"' /tmp/demo_run.ipynb


# ---- 场景 3：.Rmd → PDF ----
# 编辑器里：⇧⌘Enter 逐块跑，⇧⌘K 出 PDF。

Rscript -e 'rmarkdown::render("3-rmarkdown/demo.Rmd")'

open 3-rmarkdown/demo.pdf


# ---- 打开工作目录 ----

cursor .
