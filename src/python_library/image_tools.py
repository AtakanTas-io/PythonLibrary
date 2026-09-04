"""Görsel Optimizasyonu, Boyutlandırma ve Filigran (Watermark) Modülü."""

from pathlib import Path
from typing import List, Optional, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError

SUPPORTED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def optimize_image(
    image_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    max_width: Optional[int] = None,
    quality: int = 85,
    to_webp: bool = False,
) -> Path:
    """Görseli yeniden boyutlandırır, sıkıştırır ve opsiyonel olarak WebP formatına çevirir."""
    src = Path(image_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"Görsel bulunamadı: '{src}'")

    if src.suffix.lower() not in SUPPORTED_IMAGE_EXTS:
        raise ValidationError(f"Desteklenmeyen format: '{src.suffix}'")

    if quality < 1 or quality > 100:
        raise ValidationError("Kalite değeri 1-100 arasında olmalıdır.")

    try:
        from PIL import Image
    except ImportError as err:
        raise DependencyError("Görsel işleme için 'pillow' gereklidir.") from err

    if output_path:
        target = Path(output_path).resolve()
    else:
        new_ext = ".webp" if to_webp else src.suffix
        target = src.with_name(f"{src.stem}_opt{new_ext}")

    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(src) as img:
            # Boyutlandırma
            if max_width and img.width > max_width:
                ratio = max_width / float(img.width)
                new_height = int(float(img.height) * float(ratio))
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Format belirleme ve kaydetme
            save_format = "WEBP" if to_webp else img.format
            save_params = {"quality": quality, "optimize": True}

            if to_webp and img.mode in ("RGBA", "LA"):
                img.save(target, "WEBP", quality=quality)
            else:
                if img.mode != "RGB" and not to_webp:
                    img = img.convert("RGB")
                img.save(target, format=save_format or "JPEG", **save_params)

        return target
    except Exception as e:
        raise ConversionError(f"Görsel optimize edilirken hata oluştu: {e}") from e


def batch_optimize_images(
    folder_path: Union[str, Path],
    output_folder: Optional[Union[str, Path]] = None,
    max_width: Optional[int] = None,
    quality: int = 85,
    to_webp: bool = False,
) -> List[Path]:
    """Bir klasördeki tüm desteklenen görselleri topluca optimize eder."""
    src_dir = Path(folder_path).resolve()
    if not src_dir.exists() or not src_dir.is_dir():
        raise ValidationError(f"Klasör bulunamadı: '{src_dir}'")

    out_dir = Path(output_folder).resolve() if output_folder else src_dir / "optimized"
    out_dir.mkdir(parents=True, exist_ok=True)

    optimized_files = []
    for file in src_dir.iterdir():
        if file.is_file() and file.suffix.lower() in SUPPORTED_IMAGE_EXTS:
            out_name = f"{file.stem}.webp" if to_webp else file.name
            out_file = out_dir / out_name
            res = optimize_image(file, out_file, max_width=max_width, quality=quality, to_webp=to_webp)
            optimized_files.append(res)

    return optimized_files


def add_watermark(
    image_path: Union[str, Path],
    text: str,
    output_path: Optional[Union[str, Path]] = None,
    opacity: int = 128,
    font_size: int = 36,
) -> Path:
    """Görselin sağ alt köşesine yarı saydam metin filigranı ekler."""
    src = Path(image_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"Görsel bulunamadı: '{src}'")
    if not text or not text.strip():
        raise ValidationError("Filigran metni boş olamaz.")

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as err:
        raise DependencyError("Görsel işleme için 'pillow' gereklidir.") from err

    target = Path(output_path).resolve() if output_path else src.with_name(f"{src.stem}_watermarked{src.suffix}")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(src).convert("RGBA") as base_img:
            # Şeffaf katman oluştur
            txt_layer = Image.new("RGBA", base_img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)

            try:
                font = ImageFont.load_default()
            except Exception:
                font = None

            # Metin boyutu hesapla
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Sağ alt köşe koordinatları (10px kenar boşluğu)
            x = max(10, base_img.width - text_width - 20)
            y = max(10, base_img.height - text_height - 20)

            # Yarı saydam beyaz metin çiz
            draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

            watermarked = Image.alpha_composite(base_img, txt_layer)

            # Çıktı formatına göre kaydet
            if target.suffix.lower() in (".jpg", ".jpeg"):
                watermarked.convert("RGB").save(target, "JPEG", quality=90)
            else:
                watermarked.save(target)

        return target
    except Exception as e:
        raise ConversionError(f"Filigran eklenirken hata oluştu: {e}") from e
