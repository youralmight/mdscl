#!/usr/bin/env bash
# 一行一条命令，自己复制着跑。也可以 bash command.sh 整个跑一遍。
cd "$(dirname "${BASH_SOURCE[0]}")"


# ---- 重新生成数据（data/ 被删了或想恢复原状时跑）----

Rscript make-data.R


# ---- 看看数据长什么样 ----

head -3 data/gapminder.csv

head -6 data/gapminder-messy.csv

head -2 data/life-expectancy-wide.csv

head -4 data/measurements-long.csv


# ---- 无头跑一遍整个 notebook，确认 0 报错 ----
# 编辑器里：kernel 选 R 4.6.1，然后 ⇧Enter 一路按到底。

uvx --from nbconvert jupyter nbconvert --to notebook --execute --allow-errors --output /tmp/lec01_run.ipynb lec01-demo.ipynb

grep -c '"output_type": "error"' /tmp/lec01_run.ipynb


# ---- 打开 ----

codium .
