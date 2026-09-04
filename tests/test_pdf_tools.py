"""PDF araçları testleri."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from PIL import Image

from python_library.pdf_tools import merge_pdfs, split_pdf, images_to_pdf
from python_library.exceptions import ValidationError, DependencyError


def test_merge_pdfs_missing_dependency():
    with patch.dict(sys.modules, {"pypdf": None}):
        with pytest.raises(DependencyError, match="pypdf"):
            merge_pdfs(["a.pdf", "b.pdf"], "out.pdf")


def test_merge_pdfs_validation():
    with pytest.raises(ValidationError, match="En az iki PDF"):
        merge_pdfs(["only_one.pdf"], "out.pdf")


def test_merge_pdfs_success(tmp_path: Path):
    f1 = tmp_path / "1.pdf"
    f2 = tmp_path / "2.pdf"
    f1.write_bytes(b"%PDF-1.4 sample 1")
    f2.write_bytes(b"%PDF-1.4 sample 2")
    out_pdf = tmp_path / "merged.pdf"

    mock_merger = MagicMock()
    mock_pypdf = MagicMock()
    mock_pypdf.PdfMerger.return_value = mock_merger

    with patch.dict(sys.modules, {"pypdf": mock_pypdf}):
        res = merge_pdfs([f1, f2], out_pdf)
        assert res == out_pdf.resolve()
        assert mock_merger.append.call_count == 2
        mock_merger.write.assert_called_once_with(str(out_pdf.resolve()))
        mock_merger.close.assert_called_once()


def test_split_pdf_success(tmp_path: Path):
    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample")
    out_dir = tmp_path / "pages"

    mock_reader = MagicMock()
    mock_reader.pages = [MagicMock(), MagicMock()]  # 2 sayfa
    mock_writer = MagicMock()

    mock_pypdf = MagicMock()
    mock_pypdf.PdfReader.return_value = mock_reader
    mock_pypdf.PdfWriter.return_value = mock_writer

    with patch.dict(sys.modules, {"pypdf": mock_pypdf}):
        res = split_pdf(pdf_file, out_dir)
        assert len(res) == 2
        assert res[0].name == "page_001.pdf"
        assert res[1].name == "page_002.pdf"


def test_images_to_pdf_success(tmp_path: Path):
    img1 = tmp_path / "img1.png"
    img2 = tmp_path / "img2.png"

    Image.new("RGB", (50, 50), color="red").save(img1)
    Image.new("RGB", (50, 50), color="blue").save(img2)

    out_pdf = tmp_path / "combined.pdf"
    res = images_to_pdf([img1, img2], out_pdf)

    assert res == out_pdf.resolve()
    assert out_pdf.exists()
    assert out_pdf.stat().st_size > 0


def test_images_to_pdf_validation():
    with pytest.raises(ValidationError, match="En az bir görsel"):
        images_to_pdf([], "out.pdf")
