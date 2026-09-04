"""PythonLibrary - Çok Amaçlı Yardımcı Araçlar ve Otomasyon Kütüphanesi."""

from python_library.exceptions import (
    PythonLibraryError,
    ValidationError,
    DependencyError,
    ConversionError,
)
from python_library.qr_generator import generate_qr
from python_library.pdf_converter import convert_pdf_to_docx
from python_library.background_remover import remove_background
from python_library.water_reminder import send_notification, start_reminder_loop
from python_library.hasher import calculate_hash, verify_checksum, compare_files
from python_library.crypto_tool import encrypt_text, decrypt_text, encrypt_file, decrypt_file
from python_library.password_generator import generate_password, check_password_strength
from python_library.batch_renamer import batch_rename
from python_library.base64_tool import file_to_base64, base64_to_file, text_to_base64, base64_to_text
from python_library.markdown_tool import markdown_to_html
from python_library.data_converter import (
    json_to_csv,
    csv_to_json,
    json_to_yaml,
    yaml_to_json,
    data_to_excel,
)
from python_library.pdf_tools import merge_pdfs, split_pdf, images_to_pdf
from python_library.ocr_tool import extract_text_from_image
from python_library.image_tools import optimize_image, batch_optimize_images, add_watermark
from python_library.media_downloader import download_media
from python_library.speedtest_tool import run_speedtest
from python_library.url_shortener import shorten_url, shorten_and_qr
from python_library.network_tools import get_network_info, scan_ports, dns_lookup
from python_library.content_searcher import search_in_files
from python_library.duplicate_finder import find_duplicates

__version__ = "0.3.0"
__author__ = "AtakaanShiva"

__all__ = [
    "__version__",
    "PythonLibraryError",
    "ValidationError",
    "DependencyError",
    "ConversionError",
    "generate_qr",
    "convert_pdf_to_docx",
    "remove_background",
    "send_notification",
    "start_reminder_loop",
    "calculate_hash",
    "verify_checksum",
    "compare_files",
    "encrypt_text",
    "decrypt_text",
    "encrypt_file",
    "decrypt_file",
    "generate_password",
    "check_password_strength",
    "batch_rename",
    "file_to_base64",
    "base64_to_file",
    "text_to_base64",
    "base64_to_text",
    "markdown_to_html",
    "json_to_csv",
    "csv_to_json",
    "json_to_yaml",
    "yaml_to_json",
    "data_to_excel",
    "merge_pdfs",
    "split_pdf",
    "images_to_pdf",
    "extract_text_from_image",
    "optimize_image",
    "batch_optimize_images",
    "add_watermark",
    "download_media",
    "run_speedtest",
    "shorten_url",
    "shorten_and_qr",
    "get_network_info",
    "scan_ports",
    "dns_lookup",
    "search_in_files",
    "find_duplicates",
]
