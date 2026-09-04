"""Veri formatı dönüştürücü modülü testleri."""

import json
from pathlib import Path
import pytest
from python_library.data_converter import (
    json_to_csv,
    csv_to_json,
    json_to_yaml,
    yaml_to_json,
    data_to_excel,
)
from python_library.exceptions import ValidationError


def test_json_and_csv_roundtrip(tmp_path: Path):
    data = [
        {"id": "1", "name": "Ali", "role": "Mühendis"},
        {"id": "2", "name": "Ayşe", "role": "Yönetici"},
    ]
    json_file = tmp_path / "people.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    csv_file = json_to_csv(json_file)
    assert csv_file.exists()

    recovered_json = csv_to_json(csv_file, json_path=tmp_path / "recovered.json")
    assert recovered_json.exists()
    recovered_data = json.loads(recovered_json.read_text(encoding="utf-8"))
    assert recovered_data == data


def test_json_and_yaml_roundtrip(tmp_path: Path):
    data = {"server": {"host": "localhost", "port": 8080}, "active": True}
    json_file = tmp_path / "config.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    yaml_file = json_to_yaml(json_file)
    assert yaml_file.exists()

    recovered_json = yaml_to_json(yaml_file, json_path=tmp_path / "config_back.json")
    recovered_data = json.loads(recovered_json.read_text(encoding="utf-8"))
    assert recovered_data == data


def test_data_to_excel(tmp_path: Path):
    data = [{"title": "A", "score": 90}, {"title": "B", "score": 85}]
    json_file = tmp_path / "scores.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    excel_file = data_to_excel(json_file)
    assert excel_file.exists()
    assert excel_file.suffix == ".xlsx"
    assert excel_file.stat().st_size > 0


def test_json_to_csv_invalid_format(tmp_path: Path):
    bad_json = tmp_path / "bad.json"
    bad_json.write_text(json.dumps({"key": "not a list"}), encoding="utf-8")
    with pytest.raises(ValidationError, match="boş olmayan bir liste"):
        json_to_csv(bad_json)
