uvx jupytext --to ipynb worksheet3.Rmd

uvx jupytext --to Rmd worksheet3.ipynb

rm *_yizhang_2026-*.zip *.pdf *.html
uv run quarto render *.ipynb --to pdf --execute
uv run quarto render *.ipynb --to html --execute
quarto render *.Rmd --to typst
quarto render *.Rmd --to pdf
make all && apack $(basename $PWD)_yizhang_$(date +"%Y-%m-%d_%H-%M-%S").zip *.Rmd *.ipynb *.pdf *.md *.html
