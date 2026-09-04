"""QR Kod üretici modülü testleri."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from python_library.qr_generator import generate_qr
from python_library.exceptions import ValidationError, DependencyError, ConversionError


def test_generate_qr_empty_content():
    with pytest.raises(ValidationError, match="boş olamaz"):
        generate_qr("")

    with pytest.raises(ValidationError, match="boş olamaz"):
        generate_qr("   ")


def test_generate_qr_invalid_scale():
    with pytest.raises(ValidationError, match="pozitif bir tamsayı"):
        generate_qr("https://example.com", scale=0)

    with pytest.raises(ValidationError, match="pozitif bir tamsayı"):
        generate_qr("https://example.com", scale=-2)


def test_generate_qr_unsupported_format(temp_output_dir: Path):
    target = temp_output_dir / "out.txt"
    with pytest.raises(ValidationError, match="Desteklenmeyen QR formatı"):
        # Mock pyqrcode import
        with patch.dict(sys.modules, {"pyqrcode": MagicMock()}):
            generate_qr("https://example.com", output_path=target, format="bmp")


def test_generate_qr_missing_dependency():
    with patch.dict(sys.modules, {"pyqrcode": None}):
        with pytest.raises(DependencyError, match="pyqrcode"):
            generate_qr("https://example.com")


def test_generate_qr_svg_success(temp_output_dir: Path):
    target = temp_output_dir / "test.svg"
    mock_qr = MagicMock()
    mock_pyqrcode = MagicMock()
    mock_pyqrcode.create.return_value = mock_qr

    def fake_svg(file_path, scale):
        Path(file_path).write_text("<svg>mock_qr</svg>", encoding="utf-8")

    mock_qr.svg.side_effect = fake_svg

    with patch.dict(sys.modules, {"pyqrcode": mock_pyqrcode}):
        result = generate_qr("https://example.com", output_path=target, scale=6, format="svg")

        assert result == target.resolve()
        assert result.exists()
        assert "<svg>mock_qr</svg>" in result.read_text(encoding="utf-8")
        mock_pyqrcode.create.assert_called_once_with("https://example.com")
        mock_qr.svg.assert_called_once_with(str(target.resolve()), scale=6)


def test_generate_qr_png_success(temp_output_dir: Path):
    target = temp_output_dir / "test.png"
    mock_qr = MagicMock()
    mock_pyqrcode = MagicMock()
    mock_pyqrcode.create.return_value = mock_qr

    def fake_png(file_path, scale):
        Path(file_path).write_bytes(b"\x89PNG\r\n\x1a\n")

    mock_qr.png.side_effect = fake_png

    with patch.dict(sys.modules, {"pyqrcode": mock_pyqrcode}):
        result = generate_qr("test_content", output_path=target, format="png")
        assert result.exists()
        mock_qr.png.assert_called_once()


def test_generate_qr_conversion_error(temp_output_dir: Path):
    target = temp_output_dir / "fail.svg"
    mock_qr = MagicMock()
    mock_pyqrcode = MagicMock()
    mock_pyqrcode.create.return_value = mock_qr
    mock_qr.svg.side_effect = IOError("Disk full")

    with patch.dict(sys.modules, {"pyqrcode": mock_pyqrcode}):
        with pytest.raises(ConversionError, match="beklenmeyen bir hata"):
            generate_qr("test", output_path=target)
