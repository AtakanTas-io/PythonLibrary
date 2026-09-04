"""Görsel Arka Plan Kaldırıcı Modülü."""

from pathlib import Path
from typing import Optional, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def remove_background(
    input_image_path: Union[str, Path],
    output_image_path: Optional[Union[str, Path]] = None,
) -> Path:
    """Görselin arka planını yapay zeka tabanlı olarak kaldırır ve PNG formatında kaydeder.

    Args:
        input_image_path (Union[str, Path]): Kaynak görsel dosya yolu.
        output_image_path (Optional[Union[str, Path]]): Çıktı dosya yolu.
            Belirtilmezse kaynak ile aynı dizinde '[isim]_no_bg.png' oluşturulur.

    Returns:
        Path: Arka planı temizlenmiş PNG dosyasının mutlak yolu.

    Raises:
        ValidationError: Dosya bulunamazsa veya desteklenmeyen formatta ise fırlatılır.
        DependencyError: 'rembg' kütüphanesi yüklü değilse fırlatılır.
        ConversionError: Arka plan kaldırma veya dosya yazma hatasında fırlatılır.
    """
    src_path = Path(input_image_path).resolve()
    if not src_path.exists():
        raise ValidationError(f"Kaynak görsel dosyası bulunamadı: '{src_path}'")
    if not src_path.is_file():
        raise ValidationError(f"Belirtilen yol geçerli bir dosya değil: '{src_path}'")
    if src_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValidationError(
            f"Desteklenmeyen görsel formatı: '{src_path.suffix}'. "
            f"Desteklenenler: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    if output_image_path is None:
        target_path = src_path.with_name(f"{src_path.stem}_no_bg.png")
    else:
        target_path = Path(output_image_path).resolve()

    target_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from rembg import remove
    except ImportError as err:
        raise DependencyError(
            "Arka plan kaldırma için 'rembg' kütüphanesi gereklidir. "
            "Lütfen 'pip install rembg' komutunu çalıştırın."
        ) from err

    try:
        input_bytes = src_path.read_bytes()
        output_bytes = remove(input_bytes)
        target_path.write_bytes(output_bytes)
    except Exception as e:
        raise ConversionError(f"Arka plan kaldırılırken hata meydana geldi: {e}") from e

    return target_path
