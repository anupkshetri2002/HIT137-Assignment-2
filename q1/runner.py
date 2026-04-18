"""Program workflow for Question 1."""

from cipher import CustomCipher
from file_manager import FileManager


class Q1Runner:
    """Coordinates Q1 workflow: encrypt, decrypt, verify."""

    @staticmethod
    def get_shift_value(prompt: str) -> int:
        while True:
            user_input = input(prompt).strip()
            try:
                return int(user_input)
            except ValueError:
                print("Please enter a valid integer value.")

    @staticmethod
    @staticmethod
    def encrypt_file(shift1: int, shift2: int) -> None:
        original_text = FileManager.read_text(FileManager.RAW_FILE)
        encrypted_text = CustomCipher.encrypt_text(original_text, shift1, shift2)
        FileManager.write_text(FileManager.ENCRYPTED_FILE, encrypted_text)

    @staticmethod
    def decrypt_file(shift1: int, shift2: int) -> None:
        encrypted_text = FileManager.read_text(FileManager.ENCRYPTED_FILE)
        decrypted_text = CustomCipher.decrypt_text(encrypted_text, shift1, shift2)
        FileManager.write_text(FileManager.DECRYPTED_FILE, decrypted_text)

    @staticmethod
    def verify_decryption() -> bool:
        original = FileManager.read_text(FileManager.RAW_FILE)
        decrypted = FileManager.read_text(FileManager.DECRYPTED_FILE)
        return original == decrypted

    @staticmethod
    def run() -> None:
        shift1 = Q1Runner.get_shift_value("Enter shift1: ")
        shift2 = Q1Runner.get_shift_value("Enter shift2: ")

        Q1Runner.encrypt_file(shift1, shift2)
        Q1Runner.decrypt_file(shift1, shift2)

        if Q1Runner.verify_decryption():
            print("Decryption successful: decrypted text matches original text.")
        else:
            print("Decryption failed: decrypted text does not match original text.")