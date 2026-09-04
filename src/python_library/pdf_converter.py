"""PDF dönüştürücü modülü (PDF -> DOCX)."""

from pathlib import Path
from typing import Optional, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError


def convert_pdf_to_docx(
    pdf_path: Union[str, Path],
    docx_path: Optional[Union[str, Path]] = None,
    start_page: int = 0,
    end_page: Optional[int] = None,
) -> Path:
    """PDF belgesini DOCX (Microsoft Word) formatına dönüştürür.

    Args:
        pdf_path (Union[str, Path]): Dönüştürülecek PDF dosyasının yolu.
        docx_path (Optional[Union[str, Path]]): Hedef docx dosya yolu.
            Belirtilmezse PDF ile aynı isimde .docx uzantılı dosya oluşturulur.
        start_page (int): Dönüştürülmeye başlanacak sayfa indeksi (0 tabanlı).
        end_page (Optional[int]): Dönüştürülecek son sayfa indeksi (None ise sonuna kadar).

    Returns:
        Path: Oluşturulan DOCX dosyasının mutlak yolu.

    Raises:
        ValidationError: Girdi dosyası bulunamazsa veya uzantısı PDF değilse fırlatılır.
        DependencyError: 'pdf2docx' kütüphanesi eksikse fırlatılır.
        ConversionError: Dönüştürme sürecinde bir hata meydana gelirse fırlatılır.
    """
    src_path = Path(pdf_path).resolve()
    if not src_path.exists():
        raise ValidationError(f"Belirtilen PDF dosyası bulunamadı: '{src_path}'")
    if not src_path.is_file():
        raise ValidationError(f"Belirtilen yol geçerli bir dosya değil: '{src_path}'")
    if src_path.suffix.lower() != ".pdf":
        raise ValidationError(f"Girdi dosyası '.pdf' uzantılı olmalıdır. Mevcut uzantı: '{src_path.suffix}'")

    if docx_path is None:
        target_path = src_path.with_suffix(".docx")
    else:
        target_path = Path(docx_path).resolve()

    target_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from pdf2docx import Converter
    except ImportError as err:
        raise DependencyError(
            "PDF dönüştürme için 'pdf2docx' kütüphanesi gereklidir. "
            "Lütfen 'pip install pdf2docx' komutunu çalıştırın."
        ) from err

    cv = None
    try:
        cv = Converter(pdf_file=str(src_path))
        cv.convert(docx_filename=str(target_path), start=start_page, end=end_page)
    except Exception as e:
        raise ConversionError(f"PDF dönüştürme işlemi sırasında hata oluştu: {e}") from e
    finally:
        if cv is not None:
            try:
                cv.close()
            except Exception:
                pass

    return target_path
