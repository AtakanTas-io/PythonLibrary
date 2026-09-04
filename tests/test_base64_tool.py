"""Base64 modülü testleri."""

from pathlib import Path
import pytest
from python_library.base64_tool import (
    file_to_base64,
    base64_to_file,
    text_to_base64,
    base64_to_text,
)
from python_library.exceptions import ValidationError


def test_text_to_base64_roundtrip():
    text = "PythonLibrary Türkçe Test 123 🚀"
    b64 = text_to_base64(text)
    assert isinstance(b64, str)
    assert b64 != text

    recovered = base64_to_text(b64)
    assert recovered == text


def test_file_to_base64_roundtrip(tmp_path: Path):
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"\x00\x01\x02\x03\xff\xfe")

    encoded = file_to_base64(sample)
    recovered_file = tmp_path / "recovered.bin"
    base64_to_file(encoded, recovered_file)

    assert recovered_file.read_bytes() == sample.read_bytes()


def test_base64_validation(tmp_path: Path):
    with pytest.raises(ValidationError, match="boş olamaz"):
        text_to_base64(None)

    with pytest.raises(ValidationError, match="boş olamaz"):
        base64_to_text("")

    with pytest.raises(ValidationError, match="bulunamadı"):
        file_to_base64(tmp_path / "non_existent.file")
