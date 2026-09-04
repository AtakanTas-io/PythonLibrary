"""Medya indirici modülü testleri."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from python_library.media_downloader import download_media
from python_library.exceptions import ValidationError, DependencyError


def test_download_media_validation():
    with pytest.raises(ValidationError, match="Geçerli bir medya URL"):
        download_media("")


def test_download_media_missing_dependency():
    with patch.dict(sys.modules, {"yt_dlp": None}):
        with pytest.raises(DependencyError, match="yt-dlp"):
            download_media("https://youtube.com/watch?v=123")


def test_download_media_success(tmp_path: Path):
    mock_ydl_instance = MagicMock()
    mock_ydl_instance.extract_info.return_value = {"title": "Test Video"}
    mock_ydl_instance.prepare_filename.return_value = str(tmp_path / "Test Video.mp4")

    # Sahte indirilen dosyayı oluştur
    (tmp_path / "Test Video.mp4").write_bytes(b"fake_mp4_data")

    mock_yt_dlp = MagicMock()
    mock_yt_dlp.YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance

    with patch.dict(sys.modules, {"yt_dlp": mock_yt_dlp}):
        res = download_media("https://youtube.com/watch?v=123", output_dir=tmp_path)
        assert res == (tmp_path / "Test Video.mp4").resolve()
