"""Pytest ortak fikstürleri ve test yapılandırması."""

import pytest
from pathlib import Path


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Testler sırasında çıktı yazmak için geçici dizin sağlar."""
    out_dir = tmp_path / "test_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Testler için sahte bir PDF dosyası oluşturur."""
    pdf_file = tmp_path / "dummy_sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content for test")
    return pdf_file


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Testler için sahte bir JPG görsel dosyası oluşturur."""
    img_file = tmp_path / "dummy_image.jpg"
    img_file.write_bytes(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00")
    return img_file
