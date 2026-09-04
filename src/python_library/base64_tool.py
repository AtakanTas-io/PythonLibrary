"""Base64 Kodlayıcı ve Çözücü Modülü (Görsel, Dosya ve Metin)."""

import base64
from pathlib import Path
from typing import Union
from python_library.exceptions import ValidationError, ConversionError


def file_to_base64(file_path: Union[str, Path]) -> str:
    """Belirtilen dosyayı Base64 metin dizgisine dönüştürür."""
    src = Path(file_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"Dosya bulunamadı: '{src}'")

    data = src.read_bytes()
    return base64.b64encode(data).decode("utf-8")


def base64_to_file(base64_str: str, output_path: Union[str, Path]) -> Path:
    """Base64 metin dizgisini çözerek hedef dosyaya yazar."""
    if not base64_str or not base64_str.strip():
        raise ValidationError("Base64 verisi boş olamaz.")

    target = Path(output_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        raw_data = base64.b64decode(base64_str.strip())
        target.write_bytes(raw_data)
        return target
    except Exception as e:
        raise ConversionError(f"Base64 çözülürken hata oluştu: {e}") from e


def text_to_base64(text: str) -> str:
    """Düz metni Base64 formatında kodlar."""
    if text is None:
        raise ValidationError("Metin boş olamaz.")
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def base64_to_text(base64_str: str) -> str:
    """Base64 formatındaki metni UTF-8 düz metne çözer."""
    if not base64_str or not base64_str.strip():
        raise ValidationError("Base64 verisi boş olamaz.")

    try:
        return base64.b64decode(base64_str.strip().encode("utf-8")).decode("utf-8")
    except Exception as e:
        raise ConversionError(f"Base64 metni çözülürken hata oluştu: {e}") from e
