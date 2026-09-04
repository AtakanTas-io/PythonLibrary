"""Yinelenen (Çift) Dosyaları Tespit Etme Modülü."""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Union
from python_library.exceptions import ValidationError
from python_library.hasher import calculate_hash


def find_duplicates(
    directory: Union[str, Path],
    recursive: bool = True,
    algorithm: str = "sha256",
) -> Dict[str, List[Path]]:
    """İçeriği (hash değeri) aynı olan çift dosyaları bulur.

    Performans için önce dosya boyutuna göre gruplama, ardından aynı boyuttakiler
    arasında hash karşılaştırması yapılır.
    """
    target_dir = Path(directory).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        raise ValidationError(f"Geçerli bir dizin bulunamadı: '{target_dir}'")

    file_generator = target_dir.rglob("*") if recursive else target_dir.glob("*")
    files_by_size: Dict[int, List[Path]] = defaultdict(list)

    for p in file_generator:
        if p.is_file():
            try:
                files_by_size[p.stat().st_size].append(p)
            except OSError:
                continue

    # Yalnızca aynı boyutta 2 veya daha fazla dosya olanları incele
    duplicates_by_hash: Dict[str, List[Path]] = defaultdict(list)

    for size, candidates in files_by_size.items():
        if len(candidates) < 2:
            continue

        for file_path in candidates:
            try:
                f_hash = calculate_hash(file_path, algorithm=algorithm)
                duplicates_by_hash[f_hash].append(file_path)
            except Exception:
                continue

    # Sadece 2 veya daha fazla kopyası olan hash'leri döndür
    return {h: paths for h, paths in duplicates_by_hash.items() if len(paths) > 1}
