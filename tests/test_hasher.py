"""Hasher modülü testleri."""

from pathlib import Path
import pytest

from python_library.hasher import calculate_hash, verify_checksum, compare_files
from python_library.exceptions import ValidationError


def test_calculate_hash_sha256(tmp_path: Path):
    test_file = tmp_path / "hello.txt"
    test_file.write_text("hello world", encoding="utf-8")

    # "hello world" SHA-256
    expected_sha256 = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    result = calculate_hash(test_file, algorithm="sha256")
    assert result == expected_sha256


def test_calculate_hash_md5(tmp_path: Path):
    test_file = tmp_path / "hello_md5.txt"
    test_file.write_text("hello world", encoding="utf-8")

    # "hello world" MD5
    expected_md5 = "5eb63bbbe01eeed093cb22bb8f5acdc3"
    assert calculate_hash(test_file, algorithm="md5") == expected_md5


def test_calculate_hash_invalid_algorithm(tmp_path: Path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("data")
    with pytest.raises(ValidationError, match="Desteklenmeyen hash algoritması"):
        calculate_hash(test_file, algorithm="sha999")


def test_calculate_hash_file_not_found(tmp_path: Path):
    with pytest.raises(ValidationError, match="Geçerli bir dosya bulunamadı"):
        calculate_hash(tmp_path / "missing.txt")


def test_verify_checksum(tmp_path: Path):
    test_file = tmp_path / "check.txt"
    test_file.write_text("checksum test")
    valid_hash = calculate_hash(test_file, "sha256")

    assert verify_checksum(test_file, valid_hash, "sha256") is True
    assert verify_checksum(test_file, "wrong_hash", "sha256") is False

    with pytest.raises(ValidationError, match="boş olamaz"):
        verify_checksum(test_file, "")


def test_compare_files(tmp_path: Path):
    f1 = tmp_path / "f1.txt"
    f2 = tmp_path / "f2.txt"
    f3 = tmp_path / "f3.txt"

    f1.write_text("same content")
    f2.write_text("same content")
    f3.write_text("different content")

    assert compare_files(f1, f2) is True
    assert compare_files(f1, f3) is False
