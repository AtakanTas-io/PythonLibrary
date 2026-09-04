"""Markdown modülü testleri."""

from pathlib import Path
import pytest
from python_library.markdown_tool import markdown_to_html
from python_library.exceptions import ValidationError


def test_markdown_to_html_from_string(tmp_path: Path):
    md_text = "# Başlık 1\n\nBu bir **kalın** metindir.\n\n- Madde 1\n- Madde 2"
    out_html = tmp_path / "result.html"

    res = markdown_to_html(md_text, output_path=out_html, styled=True, title="Test Doküman")
    assert res == out_html.resolve()
    assert out_html.exists()

    content = out_html.read_text(encoding="utf-8")
    assert "<title>Test Doküman</title>" in content
    assert "<h1>Başlık 1</h1>" in content
    assert "<strong>kalın</strong>" in content
    assert "<style>" in content


def test_markdown_to_html_from_file(tmp_path: Path):
    md_file = tmp_path / "sample.md"
    md_file.write_text("## İkinci Başlık\n\n`print('kod')`", encoding="utf-8")

    res = markdown_to_html(md_file)
    assert res.exists()
    assert res.suffix == ".html"
    assert "<code>print('kod')</code>" in res.read_text(encoding="utf-8")


def test_markdown_empty_validation():
    with pytest.raises(ValidationError, match="boş olamaz"):
        markdown_to_html("")
