"""PythonLibrary Hızlı Başlangıç (Quickstart) Örnek Betiği.

Bu dosya, kütüphanenin temel fonksiyonlarının Python kodunda nasıl çağrılacağını gösterir.
"""

from pathlib import Path
import sys

# src dizinini sistem yoluna ekle
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from python_library import (
    generate_qr,
    generate_password,
    check_password_strength,
    calculate_hash,
    encrypt_text,
    decrypt_text,
    get_network_info,
)


def main():
    print("=" * 60)
    print(" PythonLibrary Hızlı Başlangıç Örnekleri")
    print("=" * 60)

    # 1. Güçlü Parola Üretimi ve Güç Analizi
    print("\n[1] Kriptografik Güvenli Parola Üretimi:")
    pwd = generate_password(length=18)
    print(f"  Üretilen Parola: {pwd}")
    analysis = check_password_strength(pwd)
    print(f"  Güç Seviyesi: {analysis['strength']} ({analysis['score']}/5) - {analysis['entropy']} bit")

    # 2. AES-256 Metin Şifreleme ve Çözme
    print("\n[2] AES-256 Metin Şifreleme:")
    secret_message = "Gizli Proje Verisi: API_KEY_987654321"
    password = "KullaniciParolasi123!"
    encrypted = encrypt_text(secret_message, password)
    print(f"  Şifreli Metin (Base64): {encrypted[:40]}...")
    decrypted = decrypt_text(encrypted, password)
    print(f"  Çözülen Metin: {decrypted}")

    # 3. Dosya Hash Hesaplama
    print("\n[3] Dosya Hash Hesaplama (SHA-256):")
    sample_path = Path(__file__).resolve().parent / "samples" / "sample.pdf"
    if sample_path.exists():
        sha256 = calculate_hash(sample_path, "sha256")
        print(f"  Dosya: {sample_path.name}")
        print(f"  SHA-256: {sha256}")

    # 4. QR Kod Üretimi (Opsiyonel kütüphane kontrolü ile)
    print("\n[4] QR Kod Üretimi:")
    out_qr = Path(__file__).resolve().parent / "samples" / "example_qr.svg"
    try:
        res = generate_qr("https://github.com/AtakaanShiva/PythonLibrary", out_qr)
        print(f"  Oluşturulan QR Kod: {res.name}")
    except Exception as e:
        print(f"  (Not: {e})")

    print("\n" + "=" * 60)
    print(" Örnekler başarıyla tamamlandı!")
    print("=" * 60)


if __name__ == "__main__":
    main()
