"""Güçlü ve Kriptografik Rastgele Parola Üretici ve Güç Analizi Modülü."""

import math
import secrets
import string
from typing import Dict, Any
from python_library.exceptions import ValidationError

AMBIGUOUS_CHARACTERS = set("l1IO0o")


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
    exclude_ambiguous: bool = True,
) -> str:
    """Kriptografik olarak güvenli (CSPRNG) rastgele parola üretir.

    Args:
        length (int): Parola uzunluğu (minimum 6, varsayılan 16).
        use_upper (bool): Büyük harf (A-Z) içersin mi.
        use_lower (bool): Küçük harf (a-z) içersin mi.
        use_digits (bool): Rakam (0-9) içersin mi.
        use_special (bool): Özel karakter (!@#$%^&* vb.) içersin mi.
        exclude_ambiguous (bool): Karıştırılabilecek karakterleri (l, 1, I, O, 0) hariç tutsun mu.

    Returns:
        str: Üretilen güvenli parola.
    """
    if length < 6:
        raise ValidationError(f"Parola uzunluğu en az 6 karakter olmalıdır. Girilen: {length}")

    char_pool = ""
    guaranteed = []

    if use_upper:
        pool = string.ascii_uppercase
        if exclude_ambiguous:
            pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARACTERS)
        char_pool += pool
        guaranteed.append(secrets.choice(pool))

    if use_lower:
        pool = string.ascii_lowercase
        if exclude_ambiguous:
            pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARACTERS)
        char_pool += pool
        guaranteed.append(secrets.choice(pool))

    if use_digits:
        pool = string.digits
        if exclude_ambiguous:
            pool = "".join(c for c in pool if c not in AMBIGUOUS_CHARACTERS)
        char_pool += pool
        guaranteed.append(secrets.choice(pool))

    if use_special:
        pool = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        char_pool += pool
        guaranteed.append(secrets.choice(pool))

    if not char_pool:
        raise ValidationError("En az bir karakter türü (büyük, küçük, rakam veya özel) seçilmelidir.")

    # Kalan karakterleri havuzdan rastgele seç
    remaining = [secrets.choice(char_pool) for _ in range(length - len(guaranteed))]
    password_list = guaranteed + remaining

    # Karakter dizilimini rastgele karıştır
    shuffled = []
    while password_list:
        idx = secrets.randbelow(len(password_list))
        shuffled.append(password_list.pop(idx))

    return "".join(shuffled)


def check_password_strength(password: str) -> Dict[str, Any]:
    """Verilen parolanın entropisini hesaplar ve güç seviyesini değerlendirir."""
    if not password:
        return {"score": 0, "strength": "Çok Zayıf", "entropy": 0.0, "feedback": "Parola boş."}

    charset_size = 0
    if any(c in string.ascii_lowercase for c in password):
        charset_size += 26
    if any(c in string.ascii_uppercase for c in password):
        charset_size += 26
    if any(c in string.digits for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32

    entropy = len(password) * math.log2(charset_size) if charset_size > 0 else 0

    if entropy < 30:
        strength = "Çok Zayıf"
        score = 1
    elif entropy < 50:
        strength = "Zayıf"
        score = 2
    elif entropy < 70:
        strength = "Orta"
        score = 3
    elif entropy < 90:
        strength = "Güçlü"
        score = 4
    else:
        strength = "Çok Güçlü"
        score = 5

    return {
        "score": score,
        "strength": strength,
        "entropy": round(entropy, 2),
        "length": len(password),
    }
