from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


import markdown
import pymupdf

if sys.platform == "darwin" and Path("/opt/homebrew/lib").is_dir():
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
        f"/opt/homebrew/lib:{os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')}".rstrip(":")
    )

from weasyprint import CSS, HTML

DEFAULT_DPI = 200
DEFAULT_FONT_SIZE_PT = 8
FONT_SIZES_PT = (DEFAULT_FONT_SIZE_PT, 9, 10)
MAX_PNG_BYTES = 5 * 1024 * 1024

_CODE_SPAN = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)
_MATH_MARKUP = (
    (re.compile(r"\\[\(\[]"), r"\( \) / \[ \]"),
    (re.compile(r"\$\$"), "$$"),
    (re.compile(r"\$[^$\n]+\$"), "$...$"),
)


def _reject_math_markup(source: Path, text: str) -> None:
    """Refuse LaTeX math: this renderer has no math engine and would print it literally."""
    outside_code = _CODE_SPAN.sub(" ", text)
    found = [label for pattern, label in _MATH_MARKUP if pattern.search(outside_code)]
    if found:
        raise ValueError(
            f"{source} contains LaTeX math markup ({', '.join(found)}); this renderer has no "
            "math engine and would print it as literal text. Write formulas as plain text "
            "instead — see admin/quiz-cheatsheet-workflow.md."
        )


def _css(columns: int, font_size_pt: int) -> str:
    return f"""
@page {{ size: Letter; margin: 0.25in; }}
html {{ font-family: Arial, "PingFang SC", sans-serif; }}
body {{ margin: 0; color: #111; font-size: {font_size_pt}pt; line-height: 1; }}
main {{ column-count: {columns}; column-fill: auto; column-gap: 0.08in; }}
h1 {{ column-span: all; margin: 0 0 2pt; font-size: 1.5em; line-height: 1; }}
h2 {{ margin: 2pt 0 0.5pt; font-size: 1.25em; line-height: 1; break-after: avoid; }}
h3 {{ margin: 1.5pt 0 0.5pt; font-size: 1.0625em; line-height: 1; break-after: avoid; }}
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
    font_size_pt: int = DEFAULT_FONT_SIZE_PT,
    dpi: int = DEFAULT_DPI,
) -> tuple[Path, Path, tuple[Path, ...], int, int, int]:
    source = source.resolve()
    output_stem = output_stem.resolve()
    if source.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError(f"Expected Markdown input, got: {source}")
    if font_size_pt not in FONT_SIZES_PT:
        raise ValueError(
            f"Font size must be one of {FONT_SIZES_PT}, got {font_size_pt}"
        )
    if dpi < 150:
        raise ValueError("DPI must be at least 150 for readable printed text")

    # Parse the source once for every column candidate.
    text = source.read_text(encoding="utf-8")
    _reject_math_markup(source, text)
    body = markdown.markdown(text, extensions=["extra", "sane_lists"])
    html = f"<!doctype html><html><body><main>{body}</main></body></html>"

    # Minimize pages; ties retain the earlier, wider column layout.
    selected_document = None
    selected_columns = None
    selected_page_count = None
    for columns in (2, 3, 4):
        document = HTML(string=html, base_url=str(source.parent)).render(
            stylesheets=[CSS(string=_css(columns, font_size_pt))]
        )
        page_count = len(document.pages)
        if selected_page_count is None or page_count < selected_page_count:
            selected_document = document
            selected_columns = columns
            selected_page_count = page_count
        if page_count == 1:
            break

    if (
        selected_document is None
        or selected_columns is None
        or selected_page_count is None
    ):
        raise RuntimeError("No column candidates were evaluated")

    # Save the selected layout and complete Letter PDF.
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    html_path = output_stem.with_suffix(".html")
    pdf_path = output_stem.with_suffix(".pdf")
    stylesheet = _css(selected_columns, font_size_pt)
    html_path.write_text(
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        f"<base href=\"{source.parent.as_uri()}/\"><style>{stylesheet}</style>"
        f"</head><body><main>{body}</main></body></html>",
        encoding="utf-8",
    )
    selected_document.write_pdf(pdf_path)

    # Render every PDF page; a one-page Cheat Sheet keeps the simple .png name.
    single_png_path = output_stem.with_suffix(".png")
    for stale_path in output_stem.parent.glob(f"{output_stem.name}-page-*.png"):
        stale_path.unlink()
    if selected_page_count == 1:
        png_paths = (single_png_path,)
    else:
        single_png_path.unlink(missing_ok=True)
        png_paths = tuple(
            output_stem.parent / f"{output_stem.name}-page-{page_number}.png"
            for page_number in range(1, selected_page_count + 1)
        )

    with pymupdf.open(pdf_path) as pdf:
        if len(pdf) != selected_page_count:
            raise RuntimeError(
                f"Expected {selected_page_count} PDF page(s), got {len(pdf)}"
            )
        expected_width_pt, expected_height_pt = 612, 792
        for page, png_path in zip(pdf, png_paths, strict=True):
            if (
                abs(page.rect.width - expected_width_pt) > 0.5
                or abs(page.rect.height - expected_height_pt) > 0.5
            ):
                raise RuntimeError(
                    f"Expected US Letter PDF, got {page.rect.width:.1f} × "
                    f"{page.rect.height:.1f} pt"
                )
            pixmap = page.get_pixmap(
                dpi=dpi,
                colorspace=pymupdf.csGRAY,
                alpha=False,
            )
            pixmap.save(png_path)
            if png_path.stat().st_size > MAX_PNG_BYTES:
                raise RuntimeError(
                    f"PNG exceeds 5 MB: {png_path} "
                    f"({png_path.stat().st_size / (1024 * 1024):.2f} MB)"
                )

    return (
        html_path,
        pdf_path,
        png_paths,
        selected_page_count,
        selected_columns,
        font_size_pt,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render Markdown as compact US Letter HTML, PDF, and PNG."
    )
    parser.add_argument("source", type=Path, help="Markdown content file")
    parser.add_argument("output_stem", type=Path, help="Output path without extension")
    parser.add_argument(
        "--font-size",
        type=int,
        choices=FONT_SIZES_PT,
        default=DEFAULT_FONT_SIZE_PT,
        help=f"Body font size in points; default: {DEFAULT_FONT_SIZE_PT}",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=DEFAULT_DPI,
        help=f"PNG resolution; default: {DEFAULT_DPI}",
    )
    args = parser.parse_args()

    html_path, pdf_path, png_paths, page_count, columns, font_size_pt = (
        render_cheatsheet(
            args.source,
            args.output_stem,
            font_size_pt=args.font_size,
            dpi=args.dpi,
        )
    )
    print(f"HTML: {html_path}")
    print(f"PDF: {pdf_path}")
    print(f"PDF pages: {page_count}")
    for png_path in png_paths:
        print(f"PNG: {png_path}")
    print(f"Layout: {columns} columns, {font_size_pt} pt")


if __name__ == "__main__":
    main()
