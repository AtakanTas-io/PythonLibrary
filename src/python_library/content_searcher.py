"""Belgeler İçinde Derin Metin Arama Modülü (TXT, DOCX, PDF)."""

from pathlib import Path
from typing import Any, Dict, List, Union
import zipfile
import xml.etree.ElementTree as ET
from python_library.exceptions import ValidationError


def _extract_text_from_docx(file_path: Path) -> str:
    """DOCX dosyasındaki XML word/document.xml içeriğinden ham metni ayıklar."""
    try:
        with zipfile.ZipFile(file_path) as z:
            xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)
            # w:t düğümlerindeki metinleri topla
            texts = [node.text for node in tree.iter() if node.text]
            return " ".join(texts)
    except Exception:
        return ""


def _extract_text_from_pdf(file_path: Path) -> str:
    """PDF dosyasından sayfa metinlerini ayıklar."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(file_path))
        return " ".join([page.extract_text() or "" for page in reader.pages])
    except Exception:
        return ""


def search_in_files(
    directory: Union[str, Path],
    query: str,
    file_types: List[str] = None,
    case_sensitive: bool = False,
) -> List[Dict[str, Any]]:
    """Dizindeki metin, Word ve PDF belgeleri içerisinde arama yapar."""
    target_dir = Path(directory).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        raise ValidationError(f"Geçerli bir arama dizini bulunamadı: '{target_dir}'")
    if not query or not query.strip():
        raise ValidationError("Arama sorgusu boş olamaz.")

    search_types = [("." + t.lstrip(".")).lower() for t in (file_types or [".txt", ".docx", ".pdf", ".md", ".json"])]
    results: List[Dict[str, Any]] = []
    target_query = query if case_sensitive else query.lower()

    for file_path in target_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in search_types:
            continue

        ext = file_path.suffix.lower()
        content = ""

        try:
            if ext in (".txt", ".md", ".json", ".csv", ".yaml", ".yml"):
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            elif ext == ".docx":
                content = _extract_text_from_docx(file_path)
            elif ext == ".pdf":
                content = _extract_text_from_pdf(file_path)
        except Exception:
            continue

        if not content:
            continue

        check_content = content if case_sensitive else content.lower()
        if target_query in check_content:
            # Eşleşen satır/paragraf kesitini al
            snippets = []
            for line in content.splitlines():
                cmp_line = line if case_sensitive else line.lower()
                if target_query in cmp_line:
                    snippets.append(line.strip())
                    if len(snippets) >= 3:
                        break

            results.append({
                "file": str(file_path),
                "filename": file_path.name,
                "matches": len(snippets),
                "snippets": snippets or [content[:120] + "..."],
            })

    return results
