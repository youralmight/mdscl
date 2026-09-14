import sys
from pathlib import Path

import pymupdf

from mdscl.cheatsheet import MAX_PNG_BYTES, main, render_cheatsheet


def test_render_cheatsheet_outputs_one_letter_page(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(
        "# Quiz Cheat Sheet\n\n## Section\n\n- concise fact\n- another fact\n",
        encoding="utf-8",
    )

    pdf_path, png_path, page_count, columns, font_size_pt, ink_bottom = (
        render_cheatsheet(
            source,
            tmp_path / "sheet",
        )
    )

    with pymupdf.open(pdf_path) as pdf:
        assert len(pdf) == 1
        assert pdf[0].rect.width == 612
        assert pdf[0].rect.height == 792
    assert page_count == 1

    assert png_path is not None
    assert ink_bottom is not None
    image = pymupdf.Pixmap(png_path)
    assert (image.width, image.height) == (1700, 2200)
    assert png_path.stat().st_size <= MAX_PNG_BYTES
    assert (columns, font_size_pt) == (2, 8)
    assert 0 < ink_bottom <= 1


def test_render_cheatsheet_outputs_multipage_pdf_without_partial_png(
    tmp_path: Path,
) -> None:
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
    stale_png = tmp_path / "sheet.png"
    stale_png.write_bytes(b"stale")

    pdf_path, png_path, page_count, _, _, ink_bottom = render_cheatsheet(
        source,
        tmp_path / "sheet",
    )

    with pymupdf.open(pdf_path) as pdf:
        assert len(pdf) == page_count
        assert page_count > 1
        assert all(page.rect.width == 612 for page in pdf)
        assert all(page.rect.height == 792 for page in pdf)

    assert png_path is None
    assert ink_bottom is None
    assert not stale_png.exists()


def test_main_reports_pdf_page_count(tmp_path: Path, monkeypatch, capsys) -> None:
    source = tmp_path / "source.md"
    source.write_text("# Quiz Cheat Sheet\n\n- concise fact\n", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mdscl-cheatsheet",
            str(source),
            str(tmp_path / "sheet"),
            "--font-size",
            "9",
        ],
    )

    main()

    output = capsys.readouterr().out.splitlines()
    assert "PDF pages: 1" in output
    assert "Layout: 2 columns, 9 pt" in output
