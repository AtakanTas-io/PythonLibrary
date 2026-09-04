"""Toplu Dosya Yeniden Adlandırıcı Modülü."""

from pathlib import Path
from typing import List, Optional, Tuple, Union
from python_library.exceptions import ValidationError


def batch_rename(
    directory: Union[str, Path],
    pattern: str = "{counter:03d}_{name}",
    extension: Optional[str] = None,
    prefix: str = "",
    suffix: str = "",
    start_counter: int = 1,
    dry_run: bool = False,
) -> List[Tuple[Path, Path]]:
    """Belirtilen dizindeki dosyaları şablona göre topluca yeniden adlandırır.

    Desteklenen şablon değişkenleri:
        {counter} : Artan sayaç numarası
        {name}    : Orijinal dosya adı (uzantısız)

    Args:
        directory (Union[str, Path]): Hedef dizin.
        pattern (str): Adlandırma şablonu (Ör: '{counter:03d}_{name}' veya 'foto_{counter}').
        extension (Optional[str]): Sadece belirli uzantıya sahip dosyaları filtrele (Ör: '.jpg').
        prefix (str): Dosya adının başına eklenecek metin.
        suffix (str): Dosya adının sonuna eklenecek metin.
        start_counter (int): Sayacın başlangıç değeri.
        dry_run (bool): True ise dosyaları gerçekten değiştirmez, sadece planlanan değişiklikleri döner.

    Returns:
        List[Tuple[Path, Path]]: (Eski Yol, Yeni Yol) çiftlerinin listesi.
    """
    target_dir = Path(directory).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        raise ValidationError(f"Geçerli bir dizin bulunamadı: '{target_dir}'")

    files = sorted([f for f in target_dir.iterdir() if f.is_file()])
    if extension:
        ext_clean = ("." + extension.lstrip(".")).lower()
        files = [f for f in files if f.suffix.lower() == ext_clean]

    renamed_pairs: List[Tuple[Path, Path]] = []
    counter = start_counter

    for file in files:
        try:
            formatted_name = pattern.format(counter=counter, name=file.stem)
        except Exception as e:
            raise ValidationError(f"Geçersiz adlandırma şablonu '{pattern}': {e}") from e

        new_filename = f"{prefix}{formatted_name}{suffix}{file.suffix}"
        new_path = file.with_name(new_filename)

        renamed_pairs.append((file, new_path))
        counter += 1

    if not dry_run:
        for old_p, new_p in renamed_pairs:
            if old_p != new_p:
                old_p.rename(new_p)

    return renamed_pairs
