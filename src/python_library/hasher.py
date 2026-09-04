"""Dosya ve Metin Hash (Sağlama Kodu) Hesaplama ve Doğrulama Modülü."""

import hashlib
from pathlib import Path
from typing import Union
from python_library.exceptions import ValidationError

SUPPORTED_ALGORITHMS = {"md5", "sha1", "sha256", "sha512"}


def calculate_hash(
    file_path: Union[str, Path],
    algorithm: str = "sha256",
    chunk_size: int = 65536,
) -> str:
    """Belirtilen dosyanın kriptografik hash özetini hesaplar.

    Args:
        file_path (Union[str, Path]): Hash hesaplanacak dosyanın yolu.
        algorithm (str): Kullanılacak algoritma ('md5', 'sha1', 'sha256', 'sha512').
        chunk_size (int): Bellek tasarrufu için blok boyutu (varsayılan: 64KB).

    Returns:
        str: Onaltılık (hex) formatında hash dizesi.

    Raises:
        ValidationError: Dosya bulunamazsa veya algoritma desteklenmiyorsa fırlatılır.
    """
    algo = algorithm.lower().strip()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValidationError(
            f"Desteklenmeyen hash algoritması: '{algorithm}'. "
            f"Desteklenenler: {', '.join(sorted(SUPPORTED_ALGORITHMS))}"
        )

    target_path = Path(file_path).resolve()
    if not target_path.exists() or not target_path.is_file():
        raise ValidationError(f"Geçerli bir dosya bulunamadı: '{target_path}'")

    hasher = getattr(hashlib, algo)()
    with open(target_path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)

    return hasher.hexdigest()


def verify_checksum(
    file_path: Union[str, Path],
    expected_hash: str,
    algorithm: str = "sha256",
) -> bool:
    """Dosyanın hash değerinin beklenen değer ile uyuşup uyuşmadığını doğrular."""
    if not expected_hash or not expected_hash.strip():
        raise ValidationError("Beklenen hash değeri boş olamaz.")

    actual_hash = calculate_hash(file_path, algorithm=algorithm)
    return actual_hash.lower() == expected_hash.strip().lower()


def compare_files(file1: Union[str, Path], file2: Union[str, Path], algorithm: str = "sha256") -> bool:
    """İki dosyanın içerik olarak birebir aynı olup olmadığını hash özetlerini kıyaslayarak belirler."""
    hash1 = calculate_hash(file1, algorithm=algorithm)
    hash2 = calculate_hash(file2, algorithm=algorithm)
    return hash1 == hash2
