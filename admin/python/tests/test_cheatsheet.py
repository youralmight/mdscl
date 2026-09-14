from pathlib import Path

import pymupdf

from mdscl.cheatsheet import MAX_PNG_BYTES, render_cheatsheet


def test_render_cheatsheet_outputs_one_letter_page(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(
        "# Quiz Cheat Sheet\n\n## Section\n\n- concise fact\n- another fact\n",
        encoding="utf-8",
    )

    pdf_path, png_path, columns, font_size_pt, ink_bottom = render_cheatsheet(
        source,
        tmp_path / "sheet",
    )

    with pymupdf.open(pdf_path) as pdf:
        assert len(pdf) == 1
        assert pdf[0].rect.width == 612
        assert pdf[0].rect.height == 792

    image = pymupdf.Pixmap(png_path)
    assert (image.width, image.height) == (1700, 2200)
    assert png_path.stat().st_size <= MAX_PNG_BYTES
    assert (columns, font_size_pt) == (2, 10)
    assert 0 < ink_bottom <= 1
