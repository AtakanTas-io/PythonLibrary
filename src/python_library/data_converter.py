"""JSON, YAML, CSV ve Excel Arasında Evrensel Veri Dönüştürücü Modülü."""

import csv
import json
from pathlib import Path
from typing import Any, List, Optional, Union
from python_library.exceptions import DependencyError, ValidationError, ConversionError


def json_to_csv(json_path: Union[str, Path], csv_path: Optional[Union[str, Path]] = None) -> Path:
    """JSON liste dosyasını CSV formatına dönüştürür."""
    src = Path(json_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"JSON dosyası bulunamadı: '{src}'")

    target = Path(csv_path).resolve() if csv_path else src.with_suffix(".csv")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list) or not data:
            raise ValidationError("JSON kök elemanı boş olmayan bir liste ([{...}, ...]) olmalıdır.")

        keys = list(data[0].keys())
        with open(target, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

        return target
    except ValidationError:
        raise
    except Exception as e:
        raise ConversionError(f"JSON -> CSV dönüştürme hatası: {e}") from e


def csv_to_json(csv_path: Union[str, Path], json_path: Optional[Union[str, Path]] = None) -> Path:
    """CSV dosyasını JSON listesine dönüştürür."""
    src = Path(csv_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"CSV dosyası bulunamadı: '{src}'")

    target = Path(json_path).resolve() if json_path else src.with_suffix(".json")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        data: List[dict] = []
        with open(src, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(dict(row))

        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return target
    except Exception as e:
        raise ConversionError(f"CSV -> JSON dönüştürme hatası: {e}") from e


def json_to_yaml(json_path: Union[str, Path], yaml_path: Optional[Union[str, Path]] = None) -> Path:
    """JSON dosyasını YAML formatına dönüştürür."""
    src = Path(json_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"JSON dosyası bulunamadı: '{src}'")

    try:
        import yaml
    except ImportError as err:
        raise DependencyError("YAML işlemleri için 'PyYAML' kütüphanesi gereklidir.") from err

    target = Path(yaml_path).resolve() if yaml_path else src.with_suffix(".yaml")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(src, "r", encoding="utf-8") as f:
            data = json.load(f)

        with open(target, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

        return target
    except Exception as e:
        raise ConversionError(f"JSON -> YAML dönüştürme hatası: {e}") from e


def yaml_to_json(yaml_path: Union[str, Path], json_path: Optional[Union[str, Path]] = None) -> Path:
    """YAML dosyasını JSON formatına dönüştürür."""
    src = Path(yaml_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"YAML dosyası bulunamadı: '{src}'")

    try:
        import yaml
    except ImportError as err:
        raise DependencyError("YAML işlemleri için 'PyYAML' kütüphanesi gereklidir.") from err

    target = Path(json_path).resolve() if json_path else src.with_suffix(".json")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(src, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return target
    except Exception as e:
        raise ConversionError(f"YAML -> JSON dönüştürme hatası: {e}") from e


def data_to_excel(
    source_path: Union[str, Path],
    excel_path: Optional[Union[str, Path]] = None,
) -> Path:
    """JSON veya CSV verisini Microsoft Excel (.xlsx) tablosuna dönüştürür."""
    src = Path(source_path).resolve()
    if not src.exists() or not src.is_file():
        raise ValidationError(f"Kaynak dosya bulunamadı: '{src}'")

    try:
        import openpyxl
    except ImportError as err:
        raise DependencyError("Excel işlemleri için 'openpyxl' kütüphanesi gereklidir.") from err

    target = Path(excel_path).resolve() if excel_path else src.with_suffix(".xlsx")
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        if src.suffix.lower() == ".json":
            with open(src, "r", encoding="utf-8") as f:
                raw = json.load(f)
            rows = raw if isinstance(raw, list) else [raw]
            if not rows or not isinstance(rows[0], dict):
                raise ValidationError("JSON içeriği nesne listesi formatında olmalıdır.")
            headers = list(rows[0].keys())
            data_matrix = [[row.get(h, "") for h in headers] for row in rows]
        elif src.suffix.lower() == ".csv":
            with open(src, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                all_rows = list(reader)
            if not all_rows:
                raise ValidationError("CSV dosyası boş.")
            headers = all_rows[0]
            data_matrix = all_rows[1:]
        else:
            raise ValidationError(f"Desteklenmeyen dosya formatı: '{src.suffix}'. .json veya .csv kullanınız.")

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Veri"
        ws.append(headers)
        for row in data_matrix:
            ws.append(row)

        wb.save(target)
        return target
    except (ValidationError, DependencyError):
        raise
    except Exception as e:
        raise ConversionError(f"Excel oluşturulurken hata meydana geldi: {e}") from e
