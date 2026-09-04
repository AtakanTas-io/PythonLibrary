"""URL Kısaltıcı ve QR Kod Entegrasyon Modülü."""

from pathlib import Path
from typing import Optional, Tuple, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError
from python_library.qr_generator import generate_qr


def shorten_url(url: str, timeout: int = 10) -> str:
    """TinyURL API kullanarak uzun bağlantıları kısaltır."""
    if not url or not url.strip():
        raise ValidationError("Kısaltılacak URL boş olamaz.")

    clean_url = url.strip()
    if not clean_url.startswith(("http://", "https://")):
        clean_url = "https://" + clean_url

    try:
        import requests
    except ImportError as err:
        raise DependencyError("URL kısaltma için 'requests' gereklidir.") from err

    api_endpoint = "https://tinyurl.com/api-create.php"
    try:
        response = requests.get(api_endpoint, params={"url": clean_url}, timeout=timeout)
        response.raise_for_status()
        shortened = response.text.strip()
        if not shortened.startswith("http"):
            raise ConversionError(f"Geçersiz API yanıtı: {shortened}")
        return shortened
    except requests.RequestException as e:
        raise ConversionError(f"URL kısaltılırken ağ hatası oluştu: {e}") from e


def shorten_and_qr(
    url: str,
    qr_output: Optional[Union[str, Path]] = None,
    scale: int = 5,
) -> Tuple[str, Path]:
    """URL'yi kısaltır ve kısaltılmış halinin QR kodunu oluşturur."""
    short_link = shorten_url(url)
    target_qr = qr_output or "short_url_qr.svg"
    qr_path = generate_qr(short_link, output_path=target_qr, scale=scale)
    return short_link, qr_path
