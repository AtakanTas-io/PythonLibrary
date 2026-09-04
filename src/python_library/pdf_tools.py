"""Gelişmiş PDF İşlemleri Modülü (Birleştirme, Ayırma ve Görsellerden PDF Oluşturma)."""

from pathlib import Path
from typing import List, Optional, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError


def merge_pdfs(pdf_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> Path:
    """Birden fazla PDF belgesini tek bir PDF dosyasında birleştirir."""
    if not pdf_paths or len(pdf_paths) < 2:
        raise ValidationError("En az iki PDF dosyası belirtilmelidir.")

    try:
        from pypdf import PdfMerger
    except ImportError as err:
        raise DependencyError(
            "PDF birleştirme için 'pypdf' kütüphanesi gereklidir. "
            "Lütfen 'pip install pypdf' komutunu çalıştırın."
        ) from err

    target = Path(output_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    merger = PdfMerger()
    try:
        for p in pdf_paths:
            resolved = Path(p).resolve()
            if not resolved.exists():
                raise ValidationError(f"Birleştirilecek PDF bulunamadı: '{resolved}'")
            merger.append(str(resolved))

        merger.write(str(target))
        return target
    except ValidationError:
        raise
    except Exception as e:
        raise ConversionError(f"PDF'ler birleştirilirken hata oluştu: {e}") from e
    finally:
        merger.close()


def split_pdf(
    pdf_path: Union[str, Path],
    output_dir: Union[str, Path],
    prefix: str = "page",
) -> List[Path]:
    """Bir PDF belgesini tek tek sayfalara ayırır."""
    src = Path(pdf_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"PDF dosyası bulunamadı: '{src}'")

    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError as err:
        raise DependencyError("PDF ayırma için 'pypdf' gereklidir.") from err

    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    created_files: List[Path] = []
    try:
        reader = PdfReader(str(src))
        total_pages = len(reader.pages)

        for idx, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)
            page_path = out_dir / f"{prefix}_{idx:03d}.pdf"
            with open(page_path, "wb") as f:
                writer.write(f)
            created_files.append(page_path)

        return created_files
    except Exception as e:
        raise ConversionError(f"PDF ayrıştırılırken hata oluştu: {e}") from e


def images_to_pdf(image_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> Path:
    """JPG/PNG görsellerini sıralı olarak tek bir PDF belgesine dönüştürür."""
    if not image_paths:
        raise ValidationError("En az bir görsel dosyası belirtilmelidir.")

    try:
        from PIL import Image
    except ImportError as err:
        raise DependencyError("Görsellerden PDF oluşturmak için 'pillow' gereklidir.") from err

    target = Path(output_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    opened_images = []
    try:
        for p in image_paths:
            img_path = Path(p).resolve()
            if not img_path.exists():
                raise ValidationError(f"Görsel dosyası bulunamadı: '{img_path}'")
            img = Image.open(img_path)
            # RGBA görselleri RGB'ye çevir (PDF alfa kanalı sevmez)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            opened_images.append(img)

        first_img = opened_images[0]
        other_imgs = opened_images[1:]

        first_img.save(target, "PDF", resolution=100.0, save_all=True, append_images=other_imgs)
        return target
    except ValidationError:
        raise
    except Exception as e:
        raise ConversionError(f"Görseller PDF'e dönüştürülürken hata oluştu: {e}") from e
    finally:
        for img in opened_images:
            try:
                img.close()
            except Exception:
                pass
