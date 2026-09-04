"""Görsel araçları testleri."""

from pathlib import Path
import pytest
from PIL import Image

from python_library.image_tools import optimize_image, batch_optimize_images, add_watermark
from python_library.exceptions import ValidationError


def test_optimize_image(tmp_path: Path):
    src_img = tmp_path / "large.jpg"
    Image.new("RGB", (800, 600), color="green").save(src_img)

    out_img = tmp_path / "resized.webp"
    res = optimize_image(src_img, output_path=out_img, max_width=400, quality=75, to_webp=True)

    assert res.exists()
    with Image.open(res) as img:
        assert img.width == 400
        assert img.height == 300
        assert img.format == "WEBP"


def test_batch_optimize_images(tmp_path: Path):
    in_dir = tmp_path / "gallery"
    in_dir.mkdir()
    for i in range(3):
        Image.new("RGB", (200, 200), color="blue").save(in_dir / f"p{i}.png")

    results = batch_optimize_images(in_dir, max_width=100)
    assert len(results) == 3
    for r in results:
        assert r.exists()


def test_add_watermark(tmp_path: Path):
    src_img = tmp_path / "photo.png"
    Image.new("RGB", (300, 200), color="white").save(src_img)

    out_img = tmp_path / "watermarked.png"
    res = add_watermark(src_img, "Telif Hakki © 2026", output_path=out_img)

    assert res.exists()
    assert res.stat().st_size > 0


def test_image_tools_validation(tmp_path: Path):
    with pytest.raises(ValidationError, match="bulunamadı"):
        optimize_image(tmp_path / "missing.jpg")

    valid_img = tmp_path / "test.jpg"
    Image.new("RGB", (10, 10)).save(valid_img)

    with pytest.raises(ValidationError, match="Kalite değeri"):
        optimize_image(valid_img, quality=150)

    with pytest.raises(ValidationError, match="boş olamaz"):
        add_watermark(valid_img, "")
