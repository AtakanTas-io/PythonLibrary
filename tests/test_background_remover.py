"""Arka plan kaldırıcı modülü testleri."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from python_library.background_remover import remove_background
from python_library.exceptions import ValidationError, DependencyError, ConversionError


def test_remove_background_file_not_found(tmp_path: Path):
    missing_file = tmp_path / "not_found.jpg"
    with pytest.raises(ValidationError, match="bulunamadı"):
        remove_background(missing_file)


def test_remove_background_invalid_extension(tmp_path: Path):
    txt_file = tmp_path / "text.txt"
    txt_file.write_text("dummy")
    with pytest.raises(ValidationError, match="Desteklenmeyen görsel formatı"):
        remove_background(txt_file)


def test_remove_background_missing_dependency(sample_image: Path):
    with patch.dict(sys.modules, {"rembg": None}):
        with pytest.raises(DependencyError, match="rembg"):
            remove_background(sample_image)


def test_remove_background_success(sample_image: Path, temp_output_dir: Path):
    target_out = temp_output_dir / "output.png"
    mock_rembg = MagicMock()
    mock_rembg.remove.return_value = b"fake_png_data_without_bg"

    with patch.dict(sys.modules, {"rembg": mock_rembg}):
        result = remove_background(sample_image, target_out)

        assert result == target_out.resolve()
        assert target_out.exists()
        assert target_out.read_bytes() == b"fake_png_data_without_bg"
        mock_rembg.remove.assert_called_once()


def test_remove_background_default_filename(sample_image: Path):
    mock_rembg = MagicMock()
    mock_rembg.remove.return_value = b"fake_png_data_without_bg"

    with patch.dict(sys.modules, {"rembg": mock_rembg}):
        result = remove_background(sample_image)

        expected = sample_image.with_name(f"{sample_image.stem}_no_bg.png").resolve()
        assert result == expected
        assert expected.exists()


def test_remove_background_conversion_error(sample_image: Path, temp_output_dir: Path):
    target_out = temp_output_dir / "err.png"
    mock_rembg = MagicMock()
    mock_rembg.remove.side_effect = RuntimeError("Model inference failed")

    with patch.dict(sys.modules, {"rembg": mock_rembg}):
        with pytest.raises(ConversionError, match="hata meydana geldi"):
            remove_background(sample_image, target_out)
