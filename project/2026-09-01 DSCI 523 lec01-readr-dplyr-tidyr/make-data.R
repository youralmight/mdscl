# 生成 demo 用的数据文件。
# 数据本身来自 gapminder 包（真实数据，不是我编的），只是被写成了各种格式，
# 好让 notebook 有东西可以练 read_* 的各种参数。
#
# 跑法： Rscript make-data.R

library(tidyverse)
library(gapminder)

dir.create("data", showWarnings = FALSE)

# 取 5 个国家，让文件小到能一眼看完
subset <- gapminder |>
  filter(country %in% c("Canada", "China", "Japan", "Brazil", "Nigeria")) |>
  mutate(country = as.character(country), continent = as.character(continent))

# ---- 1. 标准 csv -----------------------------------------------------------
write_csv(subset, "data/gapminder.csv")

# ---- 2. 制表符分隔 ---------------------------------------------------------
write_tsv(subset, "data/gapminder.tsv")

# ---- 3. 分号分隔（欧洲常见）------------------------------------------------
write_delim(subset, "data/gapminder-semicolon.txt", delim = ";")

# ---- 4. 脏文件：前面有 4 行垃圾、没有表头、缺失值写成 "N/A" 和 "-99" -------
messy <- subset |>
  mutate(lifeExp = if_else(year == 1952, NA_real_, lifeExp)) |>
  mutate(across(everything(), as.character)) |>
  mutate(lifeExp = replace_na(lifeExp, "N/A"),
         gdpPercap = if_else(year == 1957, "-99", gdpPercap))

con <- file("data/gapminder-messy.csv", "w")
writeLines(c(
  "# Gapminder extract",
  "# Source: gapminder R package",
  "# Exported 2026-09-01",
  "# Missing values are coded as N/A or -99"
), con)
close(con)
write_csv(messy, "data/gapminder-messy.csv", append = TRUE, col_names = FALSE)

# ---- 5. 不整洁：年份摊成列（pivot_longer 的练习对象）-----------------------
wide <- subset |>
  select(country, year, lifeExp) |>
  pivot_wider(names_from = year, values_from = lifeExp)
write_csv(wide, "data/life-expectancy-wide.csv")

# ---- 6. 不整洁：多个变量挤在一列（pivot_wider 的练习对象）-----------------
long <- subset |>
  filter(year >= 1997) |>
  select(country, year, lifeExp, pop, gdpPercap) |>
  pivot_longer(c(lifeExp, pop, gdpPercap), names_to = "measure", values_to = "value")
write_csv(long, "data/measurements-long.csv")

cat("生成完毕：\n")
for (f in list.files("data", full.names = TRUE)) {
  cat(sprintf("  %-38s %s 行\n", f, length(readLines(f))))
}
