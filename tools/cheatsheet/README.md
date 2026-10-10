# Markdown cheatsheet renderer

Install and run this tool independently from the repository root:

```sh
uv run --project tools/cheatsheet mdscl-cheatsheet SOURCE STEM
```

`SOURCE` is a Markdown file (`.md` or `.markdown`); `STEM` is the output path without an extension. The command creates HTML, PDF, and PNG output at that stem. The input is read-only. Dependencies and environment belong to this tool, not the course environment.

The PDF uses US Letter pages with 0.25-inch margins. The renderer chooses among two, three, or four columns to minimize page count, preferring the wider layout on ties. Default body font size is 8 pt; `--font-size` accepts 8, 9, or 10 pt. PNG output defaults to 200 DPI; `--dpi` sets another resolution but cannot be below 150 DPI. Every PDF page is rendered: one-page output uses `STEM.png`, while multiple pages use `STEM-page-1.png`, `STEM-page-2.png`, and so on. Each PNG is limited to 5 MB.

There is no math engine. LaTeX math delimiters (`$...$`, `$$...$$`, `\(...\)`, `\[...\]`) are rejected outside inline and fenced code; write formulas as plain text or Unicode. This restriction prevents formulas from being silently printed as literal markup. Review every output page visually: successful rendering and reported page count do not prove the layout is readable or suitable for use.

Run this tool's regression suite with `uv run --project tools/cheatsheet --group dev pytest tools/cheatsheet/tests`.
