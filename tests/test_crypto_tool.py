"""Crypto modülü testleri."""

from pathlib import Path
import pytest

from python_library.crypto_tool import (
    encrypt_text,
    decrypt_text,
    encrypt_file,
    decrypt_file,
)
from python_library.exceptions import ValidationError, ConversionError


def test_encrypt_decrypt_text():
    secret_text = "Gizli Mesaj: 12345!@#"
    password = "SuperStrongPassword123"

    encrypted = encrypt_text(secret_text, password)
    assert encrypted != secret_text

    decrypted = decrypt_text(encrypted, password)
    assert decrypted == secret_text


def test_decrypt_text_wrong_password():
    secret_text = "Gizli Bilgi"
    encrypted = encrypt_text(secret_text, "correct_password")

    with pytest.raises(ConversionError, match="Parola hatalı"):
        decrypt_text(encrypted, "wrong_password")


def test_encrypt_text_validation():
    with pytest.raises(ValidationError, match="boş olamaz"):
        encrypt_text("", "pwd")

    with pytest.raises(ValidationError, match="boş olamaz"):
        encrypt_text("text", "")


def test_decrypt_text_validation():
    with pytest.raises(ValidationError, match="boş olamaz"):
        decrypt_text("", "pwd")

    with pytest.raises(ValidationError, match="Geçersiz şifreli veri"):
        decrypt_text("short_invalid_base64", "pwd")


def test_encrypt_decrypt_file(tmp_path: Path):
    plain_file = tmp_path / "document.txt"
    plain_file.write_text("Bu dosya çok gizlidir.", encoding="utf-8")
    password = "FileSecretKey99"

    enc_file = encrypt_file(plain_file, password)
    assert enc_file.exists()
    assert enc_file.read_bytes() != plain_file.read_bytes()

    dec_file = decrypt_file(enc_file, password, output_path=tmp_path / "restored.txt")
    assert dec_file.exists()
    assert dec_file.read_text(encoding="utf-8") == "Bu dosya çok gizlidir."


def test_encrypt_file_not_found(tmp_path: Path):
    with pytest.raises(ValidationError, match="bulunamadı"):
        encrypt_file(tmp_path / "non_existent.txt", "pwd")
