"""Çift dosya bulucu testleri."""

from pathlib import Path
import pytest
from python_library.duplicate_finder import find_duplicates
from python_library.exceptions import ValidationError


def test_find_duplicates(tmp_path: Path):
    # İki aynı içerikli dosya
    f1 = tmp_path / "original.txt"
    f2 = tmp_path / "copy.txt"
    f3 = tmp_path / "unique.txt"

    content = "Aynı içerikli test metni"
    f1.write_text(content, encoding="utf-8")
    f2.write_text(content, encoding="utf-8")
    f3.write_text("Farklı bir metin", encoding="utf-8")

    duplicates = find_duplicates(tmp_path)
    assert len(duplicates) == 1

    dup_paths = list(duplicates.values())[0]
    assert len(dup_paths) == 2
    dup_names = {p.name for p in dup_paths}
    assert "original.txt" in dup_names
    assert "copy.txt" in dup_names


def test_find_duplicates_validation(tmp_path: Path):
    with pytest.raises(ValidationError, match="Geçerli bir dizin bulunamadı"):
        find_duplicates(tmp_path / "non_dir")
