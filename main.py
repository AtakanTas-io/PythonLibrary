"""PythonLibrary ana çalıştırma betiği."""

import sys
from pathlib import Path

# src dizinini import arama yoluna ekle (yerel çalıştırmalar için)
src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from python_library.cli import main

if __name__ == "__main__":
    sys.exit(main())