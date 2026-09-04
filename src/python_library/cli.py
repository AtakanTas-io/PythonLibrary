"""PythonLibrary Komut Satırı Arayüzü (CLI) ve İnteraktif Menüsü."""

import argparse
import sys
from pathlib import Path

from python_library import (
    __version__,
    generate_qr,
    convert_pdf_to_docx,
    remove_background,
    start_reminder_loop,
    calculate_hash,
    encrypt_text,
    decrypt_text,
    generate_password,
    check_password_strength,
    batch_rename,
    file_to_base64,
    base64_to_file,
    markdown_to_html,
    data_to_excel,
    merge_pdfs,
    split_pdf,
    images_to_pdf,
    extract_text_from_image,
    optimize_image,
    add_watermark,
    download_media,
    run_speedtest,
    shorten_and_qr,
    get_network_info,
    scan_ports,
    search_in_files,
    find_duplicates,
    PythonLibraryError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python-library",
        description="PythonLibrary: Çok Amaçlı Otomasyon ve Yardımcı Araçlar Kütüphanesi",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Kullanılacak alt komut")

    # 1. QR
    qr_p = subparsers.add_parser("qr", help="Metin veya URL'den QR kod üretir.")
    qr_p.add_argument("content", help="QR kod içeriği")
    qr_p.add_argument("-o", "--output", default="qrcode.svg", help="Çıktı dosyası yolu")
    qr_p.add_argument("-s", "--scale", type=int, default=5, help="QR ölçeği")
    qr_p.add_argument("-f", "--format", choices=["svg", "png"], default="svg")

    # 2. PDF Converter
    pdf_p = subparsers.add_parser("pdf", help="PDF belgesini DOCX formatına dönüştürür.")
    pdf_p.add_argument("pdf_path", help="PDF dosya yolu")
    pdf_p.add_argument("-o", "--output", default=None, help="Çıktı DOCX yolu")

    # 3. Background Remover
    bg_p = subparsers.add_parser("remove-bg", help="Görsel arka planını kaldırır.")
    bg_p.add_argument("image_path", help="Görsel dosya yolu")
    bg_p.add_argument("-o", "--output", default=None, help="Çıktı PNG yolu")

    # 4. Reminder
    rem_p = subparsers.add_parser("reminder", help="Su hatırlatıcısını başlatır.")
    rem_p.add_argument("-i", "--interval", type=int, default=10, help="Dakika aralığı")
    rem_p.add_argument("-t", "--title", default="Su İçme Vakti! 💧")
    rem_p.add_argument("-m", "--message", default="Bir bardak su için!")

    # 5. Hasher
    hash_p = subparsers.add_parser("hash", help="Dosyanın kriptografik hash özetini hesaplar.")
    hash_p.add_argument("file_path", help="Dosya yolu")
    hash_p.add_argument("-a", "--algo", default="sha256", choices=["md5", "sha1", "sha256", "sha512"])

    # 6. Password Generator
    pwd_p = subparsers.add_parser("password", help="Güçlü rastgele parola üretir.")
    pwd_p.add_argument("-l", "--length", type=int, default=16, help="Parola uzunluğu")
    pwd_p.add_argument("--check", help="Mevcut bir parolanın gücünü analiz eder")

    # 7. Speedtest
    subparsers.add_parser("speedtest", help="İnternet bağlantı hızını test eder.")

    # 8. Network Info
    subparsers.add_parser("net-info", help="Dış IP adresi, konum ve ISP bilgilerini gösterir.")

    # 9. Shorten URL
    short_p = subparsers.add_parser("shorten", help="URL kısaltır ve QR kodunu üretir.")
    short_p.add_argument("url", help="Kısaltılacak URL")
    short_p.add_argument("-o", "--qr-output", default=None, help="QR kod dosya yolu")

    # 10. PDF Merge
    mrg_p = subparsers.add_parser("pdf-merge", help="Birden fazla PDF dosyasını birleştirir.")
    mrg_p.add_argument("files", nargs="+", help="Birleştirilecek PDF dosyaları")
    mrg_p.add_argument("-o", "--output", required=True, help="Çıktı PDF dosya yolu")

    # 11. PDF Split
    splt_p = subparsers.add_parser("pdf-split", help="PDF dosyasını sayfalara ayırır.")
    splt_p.add_argument("file", help="PDF dosyası")
    splt_p.add_argument("-o", "--output-dir", default="split_pages", help="Çıktı klasörü")

    # 12. Images to PDF
    i2p_p = subparsers.add_parser("img2pdf", help="Görselleri tek bir PDF belgesinde birleştirir.")
    i2p_p.add_argument("images", nargs="+", help="Görsel dosyaları")
    i2p_p.add_argument("-o", "--output", required=True, help="Çıktı PDF yolu")

    # 13. Image Optimizer
    opt_p = subparsers.add_parser("img-opt", help="Görseli sıkıştırır / WebP yapar.")
    opt_p.add_argument("image", help="Görsel dosya yolu")
    opt_p.add_argument("-w", "--max-width", type=int, default=None, help="Maksimum genişlik")
    opt_p.add_argument("-q", "--quality", type=int, default=85, help="Kalite (1-100)")
    opt_p.add_argument("--webp", action="store_true", help="WebP formatına dönüştür")

    # 14. Watermark
    wm_p = subparsers.add_parser("watermark", help="Görsele metin filigranı ekler.")
    wm_p.add_argument("image", help="Görsel dosya yolu")
    wm_p.add_argument("text", help="Filigran metni")
    wm_p.add_argument("-o", "--output", default=None)

    # 15. OCR
    ocr_p = subparsers.add_parser("ocr", help="Görselden metin okur.")
    ocr_p.add_argument("image", help="Görsel dosya yolu")
    ocr_p.add_argument("-l", "--lang", default="tur+eng", help="Dil kodu")

    # 16. Search in Files
    srch_p = subparsers.add_parser("search", help="Belgeler içinde metin arar.")
    srch_p.add_argument("directory", help="Aranacak dizin")
    srch_p.add_argument("query", help="Aranacak metin")

    # 17. Find Duplicates
    dup_p = subparsers.add_parser("duplicates", help="Yinelenen çift dosyaları bulur.")
    dup_p.add_argument("directory", help="Taranacak dizin")

    return parser


def interactive_menu():
    """Argüman verilmediğinde kullanıcıya sunulan interaktif menü."""
    print("=" * 60)
    print(f"       PythonLibrary v{__version__} - Araç Kütüphanesi")
    print("=" * 60)
    print("  [BELGE & PDF]")
    print("   1. PDF -> DOCX Dönüştür")
    print("   2. PDF'leri Birleştir")
    print("   3. Görsellerden PDF Oluştur")
    print("   4. Görselden Metin Oku (OCR)")
    print("  [GÖRSEL & MEDYA]")
    print("   5. QR Kod Üret")
    print("   6. Görsel Arka Planını Kaldır")
    print("   7. Görsel Boyutlandır / Sıkıştır")
    print("   8. Görsele Filigran Ekle")
    print("  [GÜVENLİK & SİSTEM]")
    print("   9. Dosya Hash Hesapla")
    print("  10. Güçlü Parola Üret")
    print("  11. Yinelenen Çift Dosyaları Bul")
    print("  [WEB & AĞ]")
    print("  12. İnternet Hız Testi Yap")
    print("  13. Dış IP ve Ağ Bilgisi Göster")
    print("  14. Link Kısalt ve QR Kodunu Al")
    print("  15. Su İçme Hatırlatıcısını Başlat")
    print("   0. Çıkış")
    print("-" * 60)

    choice = input("İşlem seçiniz (0-15): ").strip()
    if choice == "1":
        pdf = input("PDF dosyası: ").strip()
        print(f"✔ Sonuç: {convert_pdf_to_docx(pdf)}")
    elif choice == "2":
        f1 = input("1. PDF dosyası: ").strip()
        f2 = input("2. PDF dosyası: ").strip()
        out = input("Çıktı PDF yolu: ").strip()
        print(f"✔ Sonuç: {merge_pdfs([f1, f2], out)}")
    elif choice == "3":
        imgs = input("Görseller (virgülle ayırın): ").strip().split(",")
        out = input("Çıktı PDF yolu: ").strip()
        print(f"✔ Sonuç: {images_to_pdf([i.strip() for i in imgs], out)}")
    elif choice == "4":
        img = input("Görsel yolu: ").strip()
        print("Metin:", extract_text_from_image(img))
    elif choice == "5":
        content = input("URL/Metin: ").strip()
        print(f"✔ QR Kod: {generate_qr(content)}")
    elif choice == "6":
        img = input("Görsel yolu: ").strip()
        print(f"✔ Sonuç: {remove_background(img)}")
    elif choice == "7":
        img = input("Görsel yolu: ").strip()
        print(f"✔ Optimize edildi: {optimize_image(img)}")
    elif choice == "8":
        img = input("Görsel: ").strip()
        txt = input("Metin: ").strip()
        print(f"✔ Filigran eklendi: {add_watermark(img, txt)}")
    elif choice == "9":
        f = input("Dosya yolu: ").strip()
        print(f"SHA-256: {calculate_hash(f, 'sha256')}")
    elif choice == "10":
        pwd = generate_password()
        print(f"Üretilen Parola: {pwd}")
        print("Güç Analizi:", check_password_strength(pwd))
    elif choice == "11":
        d = input("Taranacak Dizin: ").strip()
        dups = find_duplicates(d)
        print(f"{len(dups)} adet kopya grup bulundu.")
    elif choice == "12":
        print("Hız testi yapılıyor...")
        print(run_speedtest())
    elif choice == "13":
        print("Ağ Bilgisi:", get_network_info())
    elif choice == "14":
        u = input("URL: ").strip()
        link, qr = shorten_and_qr(u)
        print(f"Kısaltılmış Link: {link}, QR: {qr}")
    elif choice == "15":
        start_reminder_loop(interval_minutes=15)
    elif choice == "0":
        print("Çıkış yapıldı.")
    else:
        print("Geçersiz seçim!")


def main(args=None) -> int:
    parser = build_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        try:
            interactive_menu()
            return 0
        except (KeyboardInterrupt, EOFError):
            print("\nİşlem iptal edildi.")
            return 1
        except PythonLibraryError as e:
            print(f"Hata: {e}", file=sys.stderr)
            return 1

    try:
        if parsed_args.command == "qr":
            res = generate_qr(parsed_args.content, parsed_args.output, parsed_args.scale, parsed_args.format)
            print(f"✔ QR kod oluşturuldu: {res}")
        elif parsed_args.command == "pdf":
            res = convert_pdf_to_docx(parsed_args.pdf_path, parsed_args.output)
            print(f"✔ DOCX oluşturuldu: {res}")
        elif parsed_args.command == "remove-bg":
            res = remove_background(parsed_args.image_path, parsed_args.output)
            print(f"✔ Arka plan temizlendi: {res}")
        elif parsed_args.command == "reminder":
            start_reminder_loop(
                interval_minutes=parsed_args.interval,
                title=parsed_args.title,
                message=parsed_args.message,
            )
        elif parsed_args.command == "hash":
            res = calculate_hash(parsed_args.file_path, algorithm=parsed_args.algo)
            print(f"{parsed_args.algo.upper()}: {res}")
        elif parsed_args.command == "password":
            if parsed_args.check:
                analysis = check_password_strength(parsed_args.check)
                print(f"Güç: {analysis['strength']} ({analysis['score']}/5) - Entropi: {analysis['entropy']} bit")
            else:
                pwd = generate_password(length=parsed_args.length)
                print(f"Parola: {pwd}")
        elif parsed_args.command == "speedtest":
            print("Hız testi çalıştırılıyor...")
            res = run_speedtest()
            print(f"İndirme: {res['download_mbps']} Mbps | Yükleme: {res['upload_mbps']} Mbps | Ping: {res['ping_ms']} ms")
        elif parsed_args.command == "net-info":
            info = get_network_info()
            print(f"Dış IP: {info['public_ip']} | Konum: {info['city']}, {info['country']} | Servis: {info['isp']}")
        elif parsed_args.command == "shorten":
            link, qr = shorten_and_qr(parsed_args.url, parsed_args.qr_output)
            print(f"Kısa Link: {link} | QR Kod: {qr}")
        elif parsed_args.command == "pdf-merge":
            res = merge_pdfs(parsed_args.files, parsed_args.output)
            print(f"✔ PDF'ler birleştirildi: {res}")
        elif parsed_args.command == "pdf-split":
            res = split_pdf(parsed_args.file, parsed_args.output_dir)
            print(f"✔ {len(res)} sayfa ayrıştırıldı.")
        elif parsed_args.command == "img2pdf":
            res = images_to_pdf(parsed_args.images, parsed_args.output)
            print(f"✔ PDF oluşturuldu: {res}")
        elif parsed_args.command == "img-opt":
            res = optimize_image(parsed_args.image, max_width=parsed_args.max_width, quality=parsed_args.quality, to_webp=parsed_args.webp)
            print(f"✔ Optimize edildi: {res}")
        elif parsed_args.command == "watermark":
            res = add_watermark(parsed_args.image, parsed_args.text, parsed_args.output)
            print(f"✔ Filigran eklendi: {res}")
        elif parsed_args.command == "ocr":
            text = extract_text_from_image(parsed_args.image, lang=parsed_args.lang)
            print("--- Okunan Metin ---")
            print(text)
        elif parsed_args.command == "search":
            hits = search_in_files(parsed_args.directory, parsed_args.query)
            print(f"{len(hits)} eşleşme bulundu.")
            for h in hits:
                print(f"- {h['filename']}: {h['matches']} eşleşme")
        elif parsed_args.command == "duplicates":
            dups = find_duplicates(parsed_args.directory)
            print(f"{len(dups)} adet yinelenen kopya grubu bulundu.")
            for h, paths in dups.items():
                print(f"Hash {h[:8]}... : {[p.name for p in paths]}")

        return 0
    except PythonLibraryError as e:
        print(f"Hata: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Sistem Hatası: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
