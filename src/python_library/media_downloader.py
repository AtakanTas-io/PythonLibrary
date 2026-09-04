"""Medya ve Video/MP3 İndirici Modülü."""

from pathlib import Path
from typing import Optional, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError


def download_media(
    url: str,
    output_dir: Optional[Union[str, Path]] = None,
    audio_only: bool = False,
) -> Path:
    """Belirtilen URL'den video veya ses (MP3) indirir."""
    if not url or not url.strip():
        raise ValidationError("Geçerli bir medya URL'si belirtilmelidir.")

    try:
        import yt_dlp
    except ImportError as err:
        raise DependencyError(
            "Medya indirme için 'yt-dlp' kütüphanesi gereklidir. "
            "Lütfen 'pip install yt-dlp' komutunu çalıştırın."
        ) from err

    out_folder = Path(output_dir).resolve() if output_dir else Path.cwd() / "downloads"
    out_folder.mkdir(parents=True, exist_ok=True)

    outtmpl = str(out_folder / "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
    }

    if audio_only:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        ydl_opts.update({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if audio_only:
                filename = Path(filename).with_suffix(".mp3")
            return Path(filename).resolve()
    except Exception as e:
        raise ConversionError(f"Medya indirilirken hata meydana geldi: {e}") from e
