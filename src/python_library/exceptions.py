"""Özel istisna (exception) sınıfları."""

class PythonLibraryError(Exception):
    """PythonLibrary temel hata sınıfı."""
    pass


class ValidationError(PythonLibraryError):
    """Girdi doğrulama hatası (ör. geçersiz dosya yolu, boş içerik)."""
    pass


class DependencyError(PythonLibraryError):
    """Gereken harici bir kütüphane kurulu olmadığında fırlatılır."""
    pass


class ConversionError(PythonLibraryError):
    """Dosya dönüştürme veya işleme sırasında oluşan hatalar."""
    pass
