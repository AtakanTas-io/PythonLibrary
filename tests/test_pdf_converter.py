"""PDF Dönüştürücü modülü testleri."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from python_library.pdf_converter import convert_pdf_to_docx
from python_library.exceptions import ValidationError, DependencyError, ConversionError


def test_pdf_converter_file_not_found(tmp_path: Path):
    non_existent = tmp_path / "non_existent.pdf"
    with pytest.raises(ValidationError, match="bulunamadı"):
        convert_pdf_to_docx(non_existent)


def test_pdf_converter_invalid_extension(tmp_path: Path):
    txt_file = tmp_path / "document.txt"
    txt_file.write_text("hello")
    with pytest.raises(ValidationError, match="'.pdf' uzantılı olmalıdır"):
        convert_pdf_to_docx(txt_file)


def test_pdf_converter_missing_dependency(sample_pdf: Path):
    with patch.dict(sys.modules, {"pdf2docx": None}):
        with pytest.raises(DependencyError, match="pdf2docx"):
            convert_pdf_to_docx(sample_pdf)


def test_pdf_converter_success(sample_pdf: Path, temp_output_dir: Path):
    target_docx = temp_output_dir / "converted.docx"
    mock_cv_instance = MagicMock()
    mock_converter_class = MagicMock(return_value=mock_cv_instance)

    mock_pdf2docx = MagicMock()
    mock_pdf2docx.Converter = mock_converter_class

    with patch.dict(sys.modules, {"pdf2docx": mock_pdf2docx}):
        result = convert_pdf_to_docx(sample_pdf, target_docx, start_page=1, end_page=3)

        assert result == target_docx.resolve()
        mock_converter_class.assert_called_once_with(pdf_file=str(sample_pdf.resolve()))
        mock_cv_instance.convert.assert_called_once_with(
            docx_filename=str(target_docx.resolve()), start=1, end=3
        )
        mock_cv_instance.close.assert_called_once()


def test_pdf_converter_default_output_name(sample_pdf: Path):
    mock_cv_instance = MagicMock()
    mock_converter_class = MagicMock(return_value=mock_cv_instance)
    mock_pdf2docx = MagicMock()
    mock_pdf2docx.Converter = mock_converter_class

    with patch.dict(sys.modules, {"pdf2docx": mock_pdf2docx}):
        result = convert_pdf_to_docx(sample_pdf)
        expected_target = sample_pdf.with_suffix(".docx").resolve()
        assert result == expected_target
        mock_cv_instance.convert.assert_called_once_with(
            docx_filename=str(expected_target), start=0, end=None
        )
        mock_cv_instance.close.assert_called_once()


def test_pdf_converter_error_handling_and_cleanup(sample_pdf: Path, temp_output_dir: Path):
    target_docx = temp_output_dir / "error.docx"
    mock_cv_instance = MagicMock()
    mock_cv_instance.convert.side_effect = RuntimeError("PDF parse error")
    mock_converter_class = MagicMock(return_value=mock_cv_instance)

    mock_pdf2docx = MagicMock()
    mock_pdf2docx.Converter = mock_converter_class

    with patch.dict(sys.modules, {"pdf2docx": mock_pdf2docx}):
        with pytest.raises(ConversionError, match="hata oluştu"):
            convert_pdf_to_docx(sample_pdf, target_docx)

        # Hata olsa dahi close çağrılmalıdır
        mock_cv_instance.close.assert_called_once()
