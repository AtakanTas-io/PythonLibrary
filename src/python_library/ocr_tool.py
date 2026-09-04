"""Görselden Metin Okuma (OCR) Modülü."""

from pathlib import Path
from typing import Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError


def extract_text_from_image(
    image_path: Union[str, Path],
    lang: str = "tur+eng",
) -> str:
    """Görsel içerisindeki yazıları OCR teknolojisi ile ayıklar."""
    src = Path(image_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"Görsel dosyası bulunamadı: '{src}'")

    try:
        from PIL import Image
    except ImportError as err:
        raise DependencyError("Görsel işleme için 'pillow' gereklidir.") from err

    try:
        import pytesseract
    except ImportError as err:
        raise DependencyError(
            "OCR işlemi için 'pytesseract' kütüphanesi ve Tesseract OCR motoru gereklidir. "
            "Lütfen 'pip install pytesseract' çalıştırın."
        ) from err

    try:
        with Image.open(src) as img:
            text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except Exception as e:
        raise ConversionError(f"OCR metin çıkarma sırasında hata oluştu: {e}") from e
