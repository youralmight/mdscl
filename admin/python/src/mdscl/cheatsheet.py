from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import markdown
import pymupdf

if sys.platform == "darwin" and Path("/opt/homebrew/lib").is_dir():
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
        f"/opt/homebrew/lib:{os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')}".rstrip(":")
    )

from weasyprint import CSS, HTML

LETTER_WIDTH_PT = 612
LETTER_HEIGHT_PT = 792
MAX_PNG_BYTES = 5 * 1024 * 1024
LAYOUTS = (
    (2, 10),
    (2, 9),
    (2, 8),
    (3, 10),
    (3, 9),
    (3, 8),
    (4, 10),
    (4, 9),
    (4, 8),
)


def _css(columns: int, font_size_pt: int) -> str:
    return f"""
@page {{ size: Letter; margin: 0.25in; }}
html {{ font-family: Arial, "PingFang SC", sans-serif; }}
body {{ margin: 0; color: #111; font-size: {font_size_pt}pt; line-height: 1; }}
main {{ column-count: {columns}; column-fill: auto; column-gap: 0.08in; }}
h1 {{ column-span: all; margin: 0 0 2pt; font-size: 12pt; line-height: 1; }}
h2 {{ margin: 2pt 0 0.5pt; font-size: 10pt; line-height: 1; break-after: avoid; }}
h3 {{ margin: 1.5pt 0 0.5pt; font-size: 8.5pt; line-height: 1; break-after: avoid; }}
p, ul, ol {{ margin: 0.5pt 0; }}
ul, ol {{ padding-left: 10pt; }}
li {{ margin: 0; }}
pre {{
    margin: 1pt 0;
    padding: 1pt;
    border: 0.4pt solid #bbb;
    background: #f5f5f5;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}}
code {{ font-family: Menlo, Consolas, monospace; font-size: {font_size_pt}pt; }}
table {{
    width: 100%;
    margin: 1pt 0;
    border-collapse: collapse;
    font-size: {font_size_pt}pt;
    line-height: 1;
}}
tr {{ break-inside: avoid; }}
th, td {{ border: 0.4pt solid #999; padding: 0.5pt; vertical-align: top; overflow-wrap: anywhere; }}
hr {{ margin: 1pt 0; border: 0; border-top: 0.4pt solid #999; }}
"""


def render_cheatsheet(
    source: Path,
    output_stem: Path,
    *,
    dpi: int = 200,
) -> tuple[Path, Path, int, int, float]:
    source = source.resolve()
    output_stem = output_stem.resolve()
    if source.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError(f"Expected Markdown input, got: {source}")
    if dpi < 150:
        raise ValueError("DPI must be at least 150 for readable printed text")

    body = markdown.markdown(
        source.read_text(encoding="utf-8"),
        extensions=["extra", "sane_lists"],
    )
    html = f"<!doctype html><html><body><main>{body}</main></body></html>"

    selected_document = None
    selected_layout = None
    page_counts: list[str] = []
    for columns, font_size_pt in LAYOUTS:
        document = HTML(string=html, base_url=str(source.parent)).render(
            stylesheets=[CSS(string=_css(columns, font_size_pt))]
        )
        page_counts.append(f"{columns} columns at {font_size_pt} pt: {len(document.pages)} page(s)")
        if len(document.pages) == 1:
            selected_document = document
            selected_layout = (columns, font_size_pt)
            break

    if selected_document is None or selected_layout is None:
        attempts = "\n".join(page_counts)
        raise RuntimeError(
            "Content does not fit one Letter page at the 8 pt minimum and four-column maximum:\n"
            f"{attempts}"
        )

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    pdf_path = output_stem.with_suffix(".pdf")
    png_path = output_stem.with_suffix(".png")
    selected_document.write_pdf(pdf_path)

    with pymupdf.open(pdf_path) as pdf:
        if len(pdf) != 1:
            raise RuntimeError(f"Expected one PDF page, got {len(pdf)}")
        page = pdf[0]
        if abs(page.rect.width - LETTER_WIDTH_PT) > 0.5 or abs(page.rect.height - LETTER_HEIGHT_PT) > 0.5:
            raise RuntimeError(f"Expected US Letter PDF, got {page.rect.width:.1f} × {page.rect.height:.1f} pt")
        pixmap = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY, alpha=False)
        pixmap.save(png_path)

    if png_path.stat().st_size > MAX_PNG_BYTES:
        raise RuntimeError(
            f"PNG exceeds 5 MB: {png_path.stat().st_size / (1024 * 1024):.2f} MB"
        )

    samples = pixmap.samples_mv
    ink_bottom = next(
        (
            (row + 1) / pixmap.height
            for row in range(pixmap.height - 1, -1, -1)
            if min(samples[row * pixmap.width : (row + 1) * pixmap.width]) < 245
        ),
        0.0,
    )
    columns, font_size_pt = selected_layout
    return pdf_path, png_path, columns, font_size_pt, ink_bottom


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render Markdown as a one-sided US Letter Cheat Sheet PDF and PNG."
    )
    parser.add_argument("source", type=Path, help="Markdown content file")
    parser.add_argument("output_stem", type=Path, help="Output path without extension")
    parser.add_argument("--dpi", type=int, default=200, help="PNG resolution; default: 200")
    args = parser.parse_args()

    pdf_path, png_path, columns, font_size_pt, ink_bottom = render_cheatsheet(
        args.source,
        args.output_stem,
        dpi=args.dpi,
    )
    print(f"PDF: {pdf_path}")
    print(f"PNG: {png_path}")
    print(f"Layout: {columns} columns, {font_size_pt} pt")
    print(f"Ink reaches {ink_bottom:.1%} of page height")
    print(f"PNG size: {png_path.stat().st_size / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    main()
