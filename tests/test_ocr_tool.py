"""OCR modülü testleri."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from PIL import Image

from python_library.ocr_tool import extract_text_from_image
from python_library.exceptions import ValidationError, DependencyError


def test_ocr_missing_dependency(tmp_path: Path):
    img_file = tmp_path / "test.png"
    Image.new("RGB", (20, 20)).save(img_file)

    with patch.dict(sys.modules, {"pytesseract": None}):
        with pytest.raises(DependencyError, match="pytesseract"):
            extract_text_from_image(img_file)


def test_ocr_file_not_found(tmp_path: Path):
    with pytest.raises(ValidationError, match="Görsel dosyası bulunamadı"):
        extract_text_from_image(tmp_path / "missing.png")


def test_ocr_success(tmp_path: Path):
    img_file = tmp_path / "ocr_sample.png"
    Image.new("RGB", (100, 40), color="white").save(img_file)

    mock_pytesseract = MagicMock()
    mock_pytesseract.image_to_string.return_value = "FATURA NO: 123456\n"

    with patch.dict(sys.modules, {"pytesseract": mock_pytesseract}):
        text = extract_text_from_image(img_file, lang="tur")
        assert text == "FATURA NO: 123456"
        mock_pytesseract.image_to_string.assert_called_once()
