# DSCI 523 Quiz 1

## Import, names, pipe

- CSV: `readr::read_csv("file.csv")` -> tibble (URL allowed). Delimited: `readr::read_delim(path, delim = "\t", col_names = FALSE)`; set delimiter; no header otherwise consumes row 1 as names. Metadata/preview: `read_csv(path, skip = 2, n_max = 100)` (`n_max` = data rows). Excel: `readxl::read_excel(path, sheet = "Sheet1")`; `.xlsx` is not CSV; download URL first. Write: `readr::write_csv(df, "out.csv")` (names, no row names).
- Check delimiter/header/metadata/column count/types. Backticks for `` `Mother tongue` ``; `rename(df, new = old)`; many names: `janitor::clean_names()`.
- `<-` assigns; `==` compares. `median(x = 1:10)`: named argument; `median(x <- 1:10)`: also assigns. `|>` passes left side as first argument; dplyr takes/returns a table and uses bare column names.

## dplyr and tidy shape

```r
flights |> filter(carrier %in% c("AC", "WS"), delay > 0) |>
  mutate(delay_hours = delay / 60) |> select(carrier, delay_hours) |>
  arrange(desc(delay_hours))
```

- `select(df, a, first:last)`: same rows. `filter(df, c1, c2)`: all conditions `TRUE`; comma = AND; `NA` rows drop. Set: `x %in% c("A","B")`; elementwise OR/AND: `|`, `&`, `!`—not `||`, `&&` (only element 1).
- `mutate(df, new = old * 2, old = round(old))`: add/overwrite; later expressions may use earlier ones. `arrange(df, x, desc(y))`; `slice(df, 1)` remains table; sort then slice for extreme row. `pull(df, col)` -> vector.
- **Tidy:** one observation/row, variable/column, value/cell. Define the observation first.

```r
wide |> pivot_longer(`1999`:`2000`, names_to = "year", values_to = "cases")
wide |> pivot_longer(-country, names_to = "year", values_to = "cases")
long |> pivot_wider(names_from = type, values_from = count)
```

- Column names are values -> `pivot_longer(cols, names_to, values_to)`; `cols` uses `select()` syntax (`-id`, `everything()`). Values in a column become names -> `pivot_wider(names_from, values_from)`; remaining columns identify the observation.

## R values, types, extraction

- Scalar = length-1 vector. Atomic vectors are homogeneous: logical, integer (`1L`), double (`1`), character; `c(1,"a")` -> character. Factor has `levels`; list may mix/nest; matrix is homogeneous 2-D; data frame is equal-length columns. Tibbles are data-frame subclasses; `df[,1]` may simplify only for base data frames; `df[1]` stays a table.
- Check `typeof(x)`, `class(x)`, `str(x)`, `is.integer(x)`, `as.double(x)` (may lose information). Index starts at **1**.
- `v[2:4]` -> vector. `lst[1]` -> list; `lst[[1]]` -> element; nest `lst[[6]][[3]]`. `df[rows, cols]`/`df[1]` -> table; `df[["mass"]]`/`df$mass` -> column. `y <- x`, then modify `y`: `x` unchanged (copy-on-modify).
- Arithmetic/comparisons and `& | !` are elementwise; short inputs recycle (non-multiple lengths warn). `&&`/`||` inspect element 1. `NA` is missing: arithmetic, comparison, and logical results can propagate `NA`.

## Dates, strings, factors

```r
d <- ymd("2017-01-31"); dt <- ymd_hms("2017-01-31 20:11:59")
mdy_hm("01/31/2017 08:01"); make_date(year, month, day)
year(dt); month(dt); mday(dt); yday(dt); wday(dt, label = TRUE, abbr = FALSE)
filter(holidays, holiday_date %within% interval(start, end))
```

- `ymd`/`mdy`/`dmy` -> `Date`; time helpers -> date-time (`tz` adds time zone). `today()` -> `Date`. Parse character dates before comparison; strings are not reliable dates.
- `str_*` is vectorized. `str_detect(x,"^Al")` -> logical (`==` exact only); `str_subset()` -> vector; `str_split()` -> list; `str_split_fixed(..., n=2)` -> matrix. `str_length()` is per-string count; `str_sub(x,1,3)` (assign through `str_sub(...) <- "AAA"`). `str_c(a,b,sep="-")` elementwise; `str_c(x,collapse="-")` one string; `str_replace()` replaces first match.
- Regex: `^` start, `$` end, `.` any; regex backslash in an R string: `"\\"`. `separate()` splits a table column; `unite()` combines.
- Clean text, then `factor()`. `levels(f)`, `nlevels(f)`; filter leaves unused levels -> `fct_drop(f)`. `fct_infreq()`, `fct_reorder(f,x,.fun=median)`, `fct_relevel(f,"Asia","Africa")`, `fct_rev()` set level/graph/statistical order.

## Two tables

`left_join(x, y, by = c("countries" = "country"))`; `x` is left/main; same-name keys join by default. Duplicate keys create all combinations: check uniqueness and output rows.

- `left_join`: all `x` + `y` columns; unmatched `y` = `NA`. `inner_join`: matched rows only + both columns. `full_join`: all rows/columns; unmatched side = `NA`.
- `semi_join`: matched `x` only; only `x` columns; duplicate `y` does not copy `x`. `anti_join`: unmatched `x`; only `x` columns. First three are mutating; last two filtering.
- `bind_rows()` stacks corresponding variables/types. `bind_cols()` matches row position only—prefer a keyed join unless alignment is guaranteed.

## Base control flow and final check

```r
if (x > t) { a } else if (x < t) { b } else { c }
for (item in x) print(item ^ 2)
for (i in seq_along(x)) print(x[i] ^ 2)
```

- `if` needs one logical value; `{}` for multiple statements. Use `seq_along(x)`, never `1:length(x)` (`character(0)` would yield `1:0`).
- Answer shape first (table/vector/Date/factor/value); one table -> verb; shape -> observation then pivot; two tables -> retained rows + right columns then join; convert date/string/factor types first; check names, commas, quotes, brackets, pipe.
