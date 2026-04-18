"""Custom cipher rules for Question 1."""


class CustomCipher:
    """Implements assignment encryption and decryption rules."""

    @staticmethod
    def _shift_with_wrap(char: str, shift: int, start: str) -> str:
        start_ord = ord(start)
        return chr((ord(char) - start_ord + shift) % 26 + start_ord)

    @staticmethod
    def _encrypt_char(char: str, shift1: int, shift2: int) -> str:
        if "a" <= char <= "m":
            return CustomCipher._shift_with_wrap(char, shift1 * shift2, "a")
        if "n" <= char <= "z":
            return CustomCipher._shift_with_wrap(char, -(shift1 + shift2), "a")
        if "A" <= char <= "M":
            return CustomCipher._shift_with_wrap(char, -shift1, "A")
        if "N" <= char <= "Z":
            return CustomCipher._shift_with_wrap(char, shift2 * shift2, "A")
        return char

    @staticmethod
    def _encrypt_lower_method1(char: str, shift1: int, shift2: int) -> str:
        return CustomCipher._shift_with_wrap(char, shift1 * shift2, "a")

    @staticmethod
    def _encrypt_lower_method2(char: str, shift1: int, shift2: int) -> str:
        return CustomCipher._shift_with_wrap(char, -(shift1 + shift2), "a")

    @staticmethod
    def _encrypt_upper_method1(char: str, shift1: int) -> str:
        return CustomCipher._shift_with_wrap(char, -shift1, "A")

    @staticmethod
    def _encrypt_upper_method2(char: str, shift2: int) -> str:
        return CustomCipher._shift_with_wrap(char, shift2 * shift2, "A")

    @staticmethod
    def encrypt_text(text: str, shift1: int, shift2: int) -> str:
        return "".join(CustomCipher._encrypt_char(ch, shift1, shift2) for ch in text)

    @staticmethod
    def _decrypt_char(char: str, shift1: int, shift2: int) -> str:
        if not char.isalpha():
            return char

        if char.islower():
            candidate_method1 = CustomCipher._shift_with_wrap(char, -(shift1 * shift2), "a")
            if (
                "a" <= candidate_method1 <= "m"
                and CustomCipher._encrypt_lower_method1(candidate_method1, shift1, shift2) == char
            ):
                return candidate_method1

            candidate_method2 = CustomCipher._shift_with_wrap(char, shift1 + shift2, "a")
            if (
                "n" <= candidate_method2 <= "z"
                and CustomCipher._encrypt_lower_method2(candidate_method2, shift1, shift2) == char
            ):
                return candidate_method2

            return char

        candidate_method1 = CustomCipher._shift_with_wrap(char, shift1, "A")
        if (
            "A" <= candidate_method1 <= "M"
            and CustomCipher._encrypt_upper_method1(candidate_method1, shift1) == char
        ):
            return candidate_method1

        candidate_method2 = CustomCipher._shift_with_wrap(char, -(shift2 * shift2), "A")
        if (
            "N" <= candidate_method2 <= "Z"
            and CustomCipher._encrypt_upper_method2(candidate_method2, shift2) == char
        ):
            return candidate_method2

        return char

    @staticmethod
    def decrypt_text(text: str, shift1: int, shift2: int) -> str:
        return "".join(CustomCipher._decrypt_char(ch, shift1, shift2) for ch in text)

    @staticmethod
    def is_reversible(shift1: int, shift2: int) -> bool:
        lowercase = [chr(code) for code in range(ord("a"), ord("z") + 1)]
        uppercase = [chr(code) for code in range(ord("A"), ord("Z") + 1)]

        encrypted_lower = [CustomCipher._encrypt_char(ch, shift1, shift2) for ch in lowercase]
        encrypted_upper = [CustomCipher._encrypt_char(ch, shift1, shift2) for ch in uppercase]

        return len(set(encrypted_lower)) == 26 and len(set(encrypted_upper)) == 26