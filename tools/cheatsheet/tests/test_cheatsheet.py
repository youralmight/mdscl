from pathlib import Path

import pymupdf
import pytest

from mdscl_cheatsheet.cheatsheet import MAX_PNG_BYTES, render_cheatsheet


def test_render_cheatsheet_outputs_html_pdf_and_png(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(
        "# Quiz Cheat Sheet\n\n## Section\n\n- concise fact\n- another fact\n",
        encoding="utf-8",
    )

    html_path, pdf_path, png_paths, page_count, _, _ = render_cheatsheet(
        source, tmp_path / "sheet", dpi=150
    )

    html = html_path.read_text(encoding="utf-8")
    assert "<h1>Quiz Cheat Sheet</h1>" in html
    with pymupdf.open(pdf_path) as pdf:
        assert len(pdf) == 1
        assert pdf[0].rect.width == 612
        assert pdf[0].rect.height == 792
    assert page_count == 1

    assert png_paths == (tmp_path / "sheet.png",)
    image = pymupdf.Pixmap(png_paths[0])
    assert (image.width, image.height) == (1275, 1650)
    assert png_paths[0].stat().st_size <= MAX_PNG_BYTES


def test_code_block_is_kept_in_one_column(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    filler = "\n".join(
        f"- filler item {index}: ordinary reference text keeps a stable line height."
        for index in range(84)
    )
    code_rows = "\n".join(f"CODE_ROW_{index}" for index in range(1, 7))
    source.write_text(
        f"# Layout probe\n\n## Dense section\n\n{filler}\n\n"
        f"```python\n{code_rows}\n```\n\nEnd marker.\n",
        encoding="utf-8",
    )

    _, pdf_path, _, page_count, _, _ = render_cheatsheet(source, tmp_path / "sheet")

    assert page_count == 1
    with pymupdf.open(pdf_path) as pdf:
        words = pdf[0].get_text("words")
    marker_x = {
        marker: next((word[0] for word in words if word[4] == marker), None)
        for marker in (f"CODE_ROW_{index}" for index in range(1, 7))
    }
    assert all(x is not None for x in marker_x.values())
    assert len({round(x, 1) for x in marker_x.values() if x is not None}) == 1


def test_section_heading_stays_with_first_content_block(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    filler = "\n".join(
        f"- filler item {index}: ordinary reference text keeps a stable line height."
        for index in range(84)
    )
    source.write_text(
        f"# Layout probe\n\n{filler}\n\n"
        "## SECTION_MARKER\n\nFIRST_BLOCK_MARKER stays with its heading.\n",
        encoding="utf-8",
    )

    _, pdf_path, _, page_count, _, _ = render_cheatsheet(source, tmp_path / "sheet")

    assert page_count == 1
    with pymupdf.open(pdf_path) as pdf:
        words = pdf[0].get_text("words")
    marker_x = {
        marker: next((word[0] for word in words if word[4] == marker), None)
        for marker in ("SECTION_MARKER", "FIRST_BLOCK_MARKER")
    }
    assert all(x is not None for x in marker_x.values())
    assert round(marker_x["SECTION_MARKER"], 1) == round(marker_x["FIRST_BLOCK_MARKER"], 1)


def test_render_cheatsheet_outputs_png_for_every_pdf_page(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(
        "# Full Notes\n\n"
        + "\n\n".join(
            f"## Section {index}\n\n"
            + "A dense paragraph of course material with definitions, conditions, "
            + "examples, and exceptions that must remain in the rendered document."
            for index in range(100)
        ),
        encoding="utf-8",
    )

    _, pdf_path, png_paths, page_count, _, _ = render_cheatsheet(
        source, tmp_path / "sheet", dpi=150
    )

    with pymupdf.open(pdf_path) as pdf:
        assert len(pdf) == page_count
        assert page_count > 1
        assert all(page.rect.width == 612 for page in pdf)
        assert all(page.rect.height == 792 for page in pdf)

    assert len(png_paths) == page_count
    assert png_paths == tuple(
        tmp_path / f"sheet-page-{page_number}.png"
        for page_number in range(1, page_count + 1)
    )
    for path in png_paths:
        image = pymupdf.Pixmap(path)
        assert (image.width, image.height) == (1275, 1650)
        assert path.stat().st_size <= MAX_PNG_BYTES


@pytest.mark.parametrize(
    "formula",
    ["$P(A)=1-P(A^c)$", "$$P(A)=1-P(A^c)$$", r"\(P(A)\)", r"\[P(A)\]"],
)
def test_render_cheatsheet_rejects_latex_math(tmp_path: Path, formula: str) -> None:
    source = tmp_path / "source.md"
    source.write_text(f"# Quiz Cheat Sheet\n\n- {formula}\n", encoding="utf-8")

    with pytest.raises(ValueError):
        render_cheatsheet(source, tmp_path / "sheet")


def test_render_cheatsheet_allows_dollar_signs_inside_code(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(
        "# Quiz Cheat Sheet\n\n"
        "- `df$mass` selects a column; `str_detect(x, \"tan$\")` anchors the end\n",
        encoding="utf-8",
    )

    _, pdf_path, _, _, _, _ = render_cheatsheet(source, tmp_path / "sheet")

    with pymupdf.open(pdf_path) as pdf:
        text = "".join(page.get_text() for page in pdf)
    assert "df$mass" in text
    assert "tan$" in text
