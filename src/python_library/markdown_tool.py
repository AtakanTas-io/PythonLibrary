"""Markdown -> Şık HTML Dönüştürücü Modülü."""

from pathlib import Path
from typing import Optional, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError

BASE_CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #24292e;
    max-width: 860px;
    margin: 40px auto;
    padding: 0 20px;
    background-color: #fdfdfd;
}
h1, h2, h3 { border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
code {
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: "Consolas", monospace;
    font-size: 85%;
}
pre {
    background-color: #f6f8fa;
    padding: 16px;
    overflow: auto;
    border-radius: 6px;
    border: 1px solid #e1e4e8;
}
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
th { background-color: #f2f4f8; }
blockquote {
    border-left: 4px solid #dfe2e5;
    color: #6a737d;
    padding: 0 1em;
    margin: 0;
}
"""


def markdown_to_html(
    source: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    styled: bool = True,
    title: str = "Doküman",
) -> Path:
    """Markdown metnini veya dosyasını HTML dokümanına dönüştürür."""
    try:
        from markdown_it import MarkdownIt
    except ImportError as err:
        raise DependencyError(
            "Markdown dönüştürme için 'markdown-it-py' kütüphanesi gereklidir."
        ) from err

    src_path = Path(source)
    if src_path.exists() and src_path.is_file():
        md_text = src_path.read_text(encoding="utf-8")
        if output_path is None:
            target = src_path.with_suffix(".html")
        else:
            target = Path(output_path).resolve()
    else:
        # Doğrudan metin olarak değerlendir
        md_text = str(source)
        if not md_text.strip():
            raise ValidationError("Markdown içeriği boş olamaz.")
        if output_path is None:
            target = Path("document.html").resolve()
        else:
            target = Path(output_path).resolve()

    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        md = MarkdownIt("commonmark", {"breaks": True, "html": True})
        html_body = md.render(md_text)

        css = f"<style>{BASE_CSS}</style>" if styled else ""
        full_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {css}
</head>
<body>
{html_body}
</body>
</html>"""

        target.write_text(full_html, encoding="utf-8")
        return target
    except Exception as e:
        raise ConversionError(f"HTML üretilirken hata oluştu: {e}") from e
