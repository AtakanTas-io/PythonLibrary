"""İçerik arayıcı testleri."""

from pathlib import Path
import pytest

from python_library.content_searcher import search_in_files
from python_library.exceptions import ValidationError


def test_search_in_files_success(tmp_path: Path):
    f1 = tmp_path / "notes.txt"
    f2 = tmp_path / "data.md"
    f3 = tmp_path / "other.txt"

    f1.write_text("Toplantı notu: PythonLibrary projesini geliştiriyoruz.\nİkinci satır.", encoding="utf-8")
    f2.write_text("# Başlık\nPythonLibrary çok kapsamlı oldu.", encoding="utf-8")
    f3.write_text("Burada sadece hava durumu var.", encoding="utf-8")

    hits = search_in_files(tmp_path, query="PythonLibrary")
    assert len(hits) == 2

    files_found = {h["filename"] for h in hits}
    assert "notes.txt" in files_found
    assert "data.md" in files_found


def test_search_in_files_validation(tmp_path: Path):
    with pytest.raises(ValidationError, match="boş olamaz"):
        search_in_files(tmp_path, "")

    with pytest.raises(ValidationError, match="Geçerli bir arama dizini bulunamadı"):
        search_in_files(tmp_path / "missing_dir", "query")
