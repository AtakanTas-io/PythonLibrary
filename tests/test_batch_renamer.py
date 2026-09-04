"""Toplu yeniden adlandırıcı testleri."""

from pathlib import Path
import pytest
from python_library.batch_renamer import batch_rename
from python_library.exceptions import ValidationError


def test_batch_rename_dry_run(tmp_path: Path):
    f1 = tmp_path / "a.jpg"
    f2 = tmp_path / "b.jpg"
    f1.write_text("1")
    f2.write_text("2")

    pairs = batch_rename(tmp_path, pattern="photo_{counter:02d}", extension=".jpg", dry_run=True)
    assert len(pairs) == 2
    # Dosyalar yerinde durmalı (dry run)
    assert f1.exists()
    assert f2.exists()
    assert pairs[0][1].name == "photo_01.jpg"
    assert pairs[1][1].name == "photo_02.jpg"


def test_batch_rename_actual(tmp_path: Path):
    f1 = tmp_path / "old1.txt"
    f2 = tmp_path / "old2.txt"
    f1.write_text("1")
    f2.write_text("2")

    pairs = batch_rename(tmp_path, pattern="doc_{counter}", extension="txt", dry_run=False)
    assert len(pairs) == 2
    assert not f1.exists()
    assert not f2.exists()
    assert (tmp_path / "doc_1.txt").exists()
    assert (tmp_path / "doc_2.txt").exists()


def test_batch_rename_invalid_dir(tmp_path: Path):
    with pytest.raises(ValidationError, match="Geçerli bir dizin bulunamadı"):
        batch_rename(tmp_path / "non_dir")
