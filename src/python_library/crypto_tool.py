"""AES-256 / Fernet Parola Tabanlı Veri ve Dosya Şifreleme Modülü."""

import base64
import os
from pathlib import Path
from typing import Optional, Union

from python_library.exceptions import DependencyError, ValidationError, ConversionError


def _derive_key(password: str, salt: bytes) -> bytes:
    """Paroladan PBKDF2 kullanarak 32 baytlık Fernet anahtarı türetir."""
    try:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    except ImportError as err:
        raise DependencyError(
            "Kriptografik işlemler için 'cryptography' kütüphanesi gereklidir. "
            "Lütfen 'pip install cryptography' komutunu çalıştırın."
        ) from err

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def encrypt_text(text: str, password: str) -> str:
    """Verilen metni parola ile şifreler ve Base64 formatında döndürür.

    Format: [16 bayt Salt] + [Fernet Şifreli Veri] (Base64 kodlu).
    """
    if not text:
        raise ValidationError("Şifrelenecek metin boş olamaz.")
    if not password:
        raise ValidationError("Şifreleme parolası boş olamaz.")

    try:
        from cryptography.fernet import Fernet
    except ImportError as err:
        raise DependencyError("cryptography kütüphanesi gereklidir.") from err

    salt = os.urandom(16)
    key = _derive_key(password, salt)
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(text.encode("utf-8"))

    # Salt ve ciphertext birleştirilip base64 formatında döndürülür
    combined = salt + ciphertext
    return base64.b64encode(combined).decode("utf-8")


def decrypt_text(encrypted_text: str, password: str) -> str:
    """encrypt_text ile şifrelenmiş metni parola kullanarak çözer."""
    if not encrypted_text or not encrypted_text.strip():
        raise ValidationError("Çözülecek şifreli metin boş olamaz.")
    if not password:
        raise ValidationError("Çözme parolası boş olamaz.")

    try:
        from cryptography.fernet import Fernet, InvalidToken
    except ImportError as err:
        raise DependencyError("cryptography kütüphanesi gereklidir.") from err

    try:
        try:
            combined = base64.b64decode(encrypted_text.encode("utf-8"))
        except Exception as err:
            raise ValidationError(f"Geçersiz şifreli veri formatı: {err}") from err

        if len(combined) <= 16:
            raise ValidationError("Geçersiz şifreli veri uzunluğu.")
        salt = combined[:16]
        ciphertext = combined[16:]
        key = _derive_key(password, salt)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(ciphertext)
        return decrypted.decode("utf-8")
    except InvalidToken as err:
        raise ConversionError("Parola hatalı veya şifreli veri bozulmuş.") from err
    except (ValidationError, DependencyError, ConversionError):
        raise
    except Exception as e:
        raise ConversionError(f"Metin çözülürken hata oluştu: {e}") from e


def encrypt_file(
    file_path: Union[str, Path],
    password: str,
    output_path: Optional[Union[str, Path]] = None,
) -> Path:
    """Dosyayı parola ile şifreler ve '.enc' uzantısıyla kaydeder."""
    src = Path(file_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"Şifrelenecek dosya bulunamadı: '{src}'")

    target = Path(output_path).resolve() if output_path else src.with_suffix(src.suffix + ".enc")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        from cryptography.fernet import Fernet
    except ImportError as err:
        raise DependencyError("cryptography kütüphanesi gereklidir.") from err

    salt = os.urandom(16)
    key = _derive_key(password, salt)
    fernet = Fernet(key)

    raw_data = src.read_bytes()
    encrypted_data = fernet.encrypt(raw_data)

    target.write_bytes(salt + encrypted_data)
    return target


def decrypt_file(
    encrypted_file_path: Union[str, Path],
    password: str,
    output_path: Optional[Union[str, Path]] = None,
) -> Path:
    """'.enc' uzantılı şifrelenmiş dosyayı çözer."""
    src = Path(encrypted_file_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"Çözülecek dosya bulunamadı: '{src}'")

    if output_path:
        target = Path(output_path).resolve()
    else:
        # .enc uzantısını kaldır
        stem_suffix = src.stem if src.suffix == ".enc" else f"decrypted_{src.name}"
        target = src.with_name(stem_suffix)

    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        from cryptography.fernet import Fernet, InvalidToken
    except ImportError as err:
        raise DependencyError("cryptography kütüphanesi gereklidir.") from err

    data = src.read_bytes()
    if len(data) <= 16:
        raise ValidationError("Şifreli dosya bozuk veya çok kısa.")

    salt = data[:16]
    ciphertext = data[16:]

    try:
        key = _derive_key(password, salt)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(ciphertext)
        target.write_bytes(decrypted)
        return target
    except InvalidToken as err:
        raise ConversionError("Parola hatalı veya dosya bozulmuş.") from err
    except Exception as e:
        raise ConversionError(f"Dosya çözülürken hata oluştu: {e}") from e
