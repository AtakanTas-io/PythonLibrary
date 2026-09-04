"""QR Kod Oluşturucu Modülü."""

from pathlib import Path
from typing import Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError


def generate_qr(
    content: str,
    output_path: Union[str, Path] = "qrcode.svg",
    scale: int = 5,
    format: str = "svg",
) -> Path:
    """Verilen metin/URL içeriği için bir QR kod üretir ve dosyaya kaydeder.

    Args:
        content (str): QR kod içerisine gömülecek metin veya URL.
        output_path (Union[str, Path]): Çıktı dosyasının yolu.
        scale (int): QR kod ölçek boyutu (varsayılan: 5).
        format (str): Çıktı dosya formatı ('svg' veya 'png').

    Returns:
        Path: Oluşturulan QR kod dosyasının mutlak dosya yolu.

    Raises:
        ValidationError: İçerik boşsa veya scale geçersizse fırlatılır.
        DependencyError: Gerekli pyqrcode kütüphanesi yüklü değilse fırlatılır.
        ConversionError: Dosya kaydetme esnasında bir hata oluşursa fırlatılır.
    """
    if not isinstance(content, str) or not content.strip():
        raise ValidationError("QR kod içeriği boş olamaz ve geçerli bir metin olmalıdır.")

    if scale <= 0:
        raise ValidationError(f"Ölçek (scale) değeri pozitif bir tamsayı olmalıdır. Girilen: {scale}")

    try:
        import pyqrcode
    except ImportError as err:
        raise DependencyError(
            "QR kod üretimi için 'pyqrcode' kütüphanesi gereklidir. "
            "Lütfen 'pip install pyqrcode' komutunu çalıştırın."
        ) from err

    target = Path(output_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        qr = pyqrcode.create(content.strip())
        fmt = format.lower()
        if fmt == "svg":
            qr.svg(str(target), scale=scale)
        elif fmt == "png":
            try:
                qr.png(str(target), scale=scale)
            except Exception as e:
                raise ConversionError(
                    f"PNG formatında QR kod oluşturmak için 'pypng' kütüphanesi gereklidir: {e}"
                ) from e
        else:
            raise ValidationError(f"Desteklenmeyen QR formatı: '{format}'. 'svg' veya 'png' seçiniz.")
    except (ValidationError, ConversionError):
        raise
    except Exception as e:
        raise ConversionError(f"QR kod oluşturulurken beklenmeyen bir hata meydana geldi: {e}") from e

    return target
