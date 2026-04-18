"""File operations for Question 1."""

from pathlib import Path


class FileManager:
    """Static helpers for reading and writing Q1 files."""

    BASE_DIR = Path(__file__).resolve().parent
    RAW_FILE = BASE_DIR / "raw_text.txt"
    ENCRYPTED_FILE = BASE_DIR / "encrypted_text.txt"
    DECRYPTED_FILE = BASE_DIR / "decrypted_text.txt"

    @staticmethod
    def read_text(file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")

    @staticmethod
    def write_text(file_path: Path, content: str) -> None:
        file_path.write_text(content, encoding="utf-8")