import sys
from pathlib import Path

import pymupdf

from mdscl.cheatsheet import MAX_PNG_BYTES, main, render_cheatsheet


def test_render_cheatsheet_outputs_html_pdf_and_png(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text(
        "# Quiz Cheat Sheet\n\n## Section\n\n- concise fact\n- another fact\n",
        encoding="utf-8",
    )

    html_path, pdf_path, png_paths, page_count, columns, font_size_pt = (
        render_cheatsheet(
            source,
            tmp_path / "sheet",
        )
    )

    html = html_path.read_text(encoding="utf-8")
    assert "<style>" in html
    assert "<h1>Quiz Cheat Sheet</h1>" in html
    with pymupdf.open(pdf_path) as pdf:
        assert len(pdf) == 1
        assert pdf[0].rect.width == 612
        assert pdf[0].rect.height == 792
    assert page_count == 1

    assert png_paths == (tmp_path / "sheet.png",)
    image = pymupdf.Pixmap(png_paths[0])
    assert (image.width, image.height) == (1700, 2200)
    assert png_paths[0].stat().st_size <= MAX_PNG_BYTES
    assert (columns, font_size_pt) == (2, 8)


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

    html_path, pdf_path, png_paths, page_count, _, _ = render_cheatsheet(
        source,
        tmp_path / "sheet",
    )

    assert html_path.exists()
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
        assert (image.width, image.height) == (1700, 2200)


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
    assert any(line.startswith("HTML: ") for line in output)
    assert any(line.startswith("PNG: ") for line in output)
