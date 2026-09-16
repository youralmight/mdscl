uvx jupytext --to ipynb worksheet3.Rmd

uvx jupytext --to Rmd worksheet3.ipynb


quarto render *.Rmd --to typst
make all || true
rm *_yizhang_2026-*.zip 
apack $(basename $PWD)_yizhang_$(date +"%Y-%m-%d_%H-%M-%S").zip *.Rmd *.ipynb *.pdf *.md *.html
