# 🐍 PythonLibrary

Günlük rutin işleri, dosya dönüştürme işlemlerini, veri formatlama süreçlerini, ağ analizlerini ve güvenliği otomatize etmek için geliştirilmiş modüler, test edilmiş ve genişletilebilir Python araç kütüphanesi ve CLI aracı.

---

## 🚀 Özellikler ve Modüller

### 1. 📄 Belge ve PDF Araçları
- **`qr_generator`:** Metin veya URL'den ölçeklenebilir SVG/PNG QR kod üretir.
- **`pdf_converter`:** PDF belgelerini Microsoft Word (`.docx`) formatına dönüştürür.
- **`pdf_tools`:**
  - `merge_pdfs`: Çoklu PDF dosyasını tek bir dosyada birleştirir.
  - `split_pdf`: PDF belgesini sayfa sayfa ayıklar.
  - `images_to_pdf`: JPG/PNG görsellerini sıralı tek bir PDF belgesine dönüştürür.
- **`ocr_tool`:** Görsellerdeki metinleri OCR (Tesseract) ile okuyup metin olarak ayıklar.

### 2. 🖼️ Görsel ve Medya Araçları
- **`background_remover`:** Fotoğrafların arka planını yapay zeka tabanlı (`rembg`) temizler.
- **`image_tools`:**
  - `optimize_image`: Görselleri sıkıştırır, yeniden boyutlandırır veya WebP'ye dönüştürür.
  - `batch_optimize_images`: Klasördeki tüm görselleri topluca optimize eder.
  - `add_watermark`: Görsellere yarı saydam metin filigranı ekler.
- **`media_downloader`:** YouTube ve diğer video sitelerinden video veya ses (MP3) indirir (`yt-dlp`).

### 3. 🌐 Web ve Ağ Araçları
- **`speedtest_tool`:** İnternet download, upload ve ping hızını anlık test eder (`speedtest-cli`).
- **`url_shortener`:** Uzun linkleri kısaltır ve tek komutla kısaltılmış halinin QR kodunu oluşturur.
- **`network_tools`:**
  - `get_network_info`: Dış IP adresi, şehir, ülke ve servis sağlayıcı (ISP) bilgisini getirir.
  - `scan_ports`: Hedef sunucudaki portların (80, 443, 22 vb.) açık/kapalı durumunu tarar.
  - `dns_lookup`: Alan adının DNS A, MX, TXT kayıtlarını sorgular.

### 4. 🔒 Güvenlik, Kriptografi ve Sistem
- **`hasher`:** Dosyaların MD5, SHA-1, SHA-256 ve SHA-512 hash özetlerini çıkarır, checksum doğrular ve dosyaları karşılaştırır.
- **`crypto_tool`:** Metinleri ve dosyaları AES-256 (Fernet + PBKDF2) ile parolalı şifreler (`.enc`) ve çözer.
- **`password_generator`:** Kriptografik güvenli rastgele parola üretir ve entropi/güç analizi yapar.
- **`batch_renamer`:** Klasördeki dosyaları şablona göre topluca yeniden adlandırır.
- **`water_reminder`:** Masaüstü bildirimleriyle periyodik su içme ve mola hatırlatması yapar.

### 5. 🔄 Veri Formatı ve Doküman Araçları
- **`data_converter`:** JSON ⇄ YAML ⇄ CSV ⇄ Excel (.xlsx) arasında çift yönlü veri dönüştürmesi yapar.
- **`base64_tool`:** Dosyaları ve metinleri Base64'e kodlar veya Base64'ten çözer.
- **`markdown_tool`:** `.md` dosyalarını profesyonel CSS temalı HTML dokümanına çevirir.

### 6. 🔍 İçerik Arama ve Yinelenen Dosyalar
- **`content_searcher`:** Belgelerin (TXT, DOCX, PDF, MD) içinde derinlemesine metin arar.
- **`duplicate_finder`:** İsimleri farklı olsa bile içeriği (hash değeri) aynı olan çift dosyaları tespit eder.

---

## 📁 Proje Dizin Mimarisi

```text
PythonLibrary/
├── pyproject.toml               # Modern PEP 517/518 paket yapılandırması
├── requirements.txt             # Çalışma zamanı bağımlılıkları
├── requirements-dev.txt         # Test ve geliştirici bağımlılıkları
├── README.md                    # Kapsamlı proje dokümantasyonu
├── main.py                      # Kütüphane CLI & interaktif giriş noktası
├── examples/                    # Örnek kullanım betikleri ve dosyalar
│   ├── quickstart.py            # Hızlı başlangıç örnek kodu
│   └── samples/                 # Örnek PDF, DOCX ve görsel dosyaları
├── src/
│   └── python_library/          # Ana kütüphane paket kaynak kodları
│       ├── __init__.py          # API dışa aktarımları ve sürüm bilgisi (v0.3.0)
│       ├── __main__.py          # 'python -m python_library' çalıştırma desteği
│       ├── exceptions.py        # Özel hata sınıfları
│       ├── qr_generator.py      # QR kod üretici
│       ├── pdf_converter.py     # PDF -> DOCX dönüştürücü
│       ├── pdf_tools.py         # PDF birleştirme ve ayırma
│       ├── ocr_tool.py          # Görselden metin okuma
│       ├── background_remover.py# AI arka plan temizleyici
│       ├── image_tools.py       # Görsel boyutlandırma ve filigran
│       ├── media_downloader.py  # Video / MP3 indirici
│       ├── speedtest_tool.py    # İnternet hız testi
│       ├── url_shortener.py     # URL kısaltıcı ve QR entegrasyonu
│       ├── network_tools.py     # IP, DNS ve port tarayıcı
│       ├── hasher.py            # Kriptografik hash ve doğrulama
│       ├── crypto_tool.py       # AES-256 şifreleme ve çözme
│       ├── password_generator.py# Parola üretici ve güç analizi
│       ├── batch_renamer.py     # Toplu dosya adlandırıcı
│       ├── data_converter.py    # JSON / YAML / CSV / Excel çevirici
│       ├── base64_tool.py       # Base64 dönüştürücü
│       ├── markdown_tool.py     # Markdown -> HTML çevirici
│       ├── content_searcher.py  # Belgeler içinde derin metin arama
│       ├── duplicate_finder.py  # Yinelenen çift dosya bulucu
│       ├── water_reminder.py    # Masaüstü bildirim hatırlatıcısı
│       └── cli.py               # Komut satırı ve interaktif menü
└── tests/                       # 103 adet izole edilmiş birim testi
```

---

## 🛠️ Kurulum

```bash
# Temel kütüphane ve geliştirici kurulumu
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Kütüphaneyi geliştirici modunda bağlama
pip install -e .
```

---

## 💻 Komut Satırı (CLI) Kullanımı

Uygulamayı hiçbir parametre vermeden çalıştırdığınızda **İnteraktif Menü** açılır:
```bash
python main.py
```

### Popüler Komut Satırı Örnekleri:

```bash
# 1. Güçlü parola üret (20 karakter) veya kontrol et
python main.py password -l 20
python main.py password --check "Gecersiz123"

# 2. Dosya SHA-256 Hash hesapla
python main.py hash pyproject.toml

# 3. İnternet hızını test et
python main.py speedtest

# 4. Dış IP ve Ağ bilgilerini al
python main.py net-info

# 5. Link kısalt ve QR kodunu üret
python main.py shorten "https://github.com/AtakaanShiva" -o github_qr.svg

# 6. Belgeler içinde metin ara
python main.py search . "PythonLibrary"

# 7. Çift (yinelenen) dosyaları bul
python main.py duplicates ./belgeler

# 8. Çoklu PDF dosyalarını birleştir
python main.py pdf-merge bolum1.pdf bolum2.pdf -o tam_kitap.pdf

# 9. Görseli optimize et ve WebP yap
python main.py img-opt foto.jpg --max-width 1200 --quality 80 --webp

# 10. Görsele filigran bas
python main.py watermark foto.jpg "Gizli Belge"
```

---

## 🐍 Python Kütüphanesi Olarak Kullanım (API)

```python
from python_library import (
    generate_qr,
    calculate_hash,
    generate_password,
    check_password_strength,
    encrypt_text,
    decrypt_text,
    json_to_csv,
    markdown_to_html,
    get_network_info,
    find_duplicates,
)

# Kriptografik güvenli parola üret
password = generate_password(length=18)
print("Parola:", password)
print("Güç:", check_password_strength(password))

# AES-256 Metin Şifreleme
secret = encrypt_text("Çok gizli veri", password="anahtar_kelime")
print("Çözülen:", decrypt_text(secret, password="anahtar_kelime"))

# Dosya Hash Doğrulama
sha256 = calculate_hash("dosya.pdf", algorithm="sha256")

# Veri Dönüştürme
json_to_csv("veriler.json", "veriler.csv")

# Markdown -> Şık HTML
markdown_to_html("README.md", "rapor.html")

# Ağ ve Dış IP
print(get_network_info())
```

---

## 🧪 Test Paketi ve Kalite Güvencesi (QA)

Tüm modüller, harici ağ ve işletim sistemi çağrılarından izole edilerek **103 adet birim ve entegrasyon testi** ile doğrulanmıştır:

```bash
# Testleri ve kapsam raporunu çalıştır
python -m pytest
```

---

## 📄 Lisans
Bu proje açık kaynaklıdır ve MIT lisansı ile korunmaktadır.
