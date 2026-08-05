"""
Unit Tests for Caesar Cipher
Tests encryption, decryption, and edge cases
"""

import unittest


class CaesarCipher:
    """Caesar Cipher class for testing"""
    
    @staticmethod
    def encrypt(text, shift):
        """Encrypts text using Caesar Cipher"""
        result = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                else:
                    result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                result += char
        return result
    
    @staticmethod
    def decrypt(text, shift):
        """Decrypts text using Caesar Cipher"""
        return CaesarCipher.encrypt(text, -shift)
    
    @staticmethod
    def brute_force(text):
        """Tries all possible shifts"""
        results = {}
        for shift in range(1, 26):
            results[shift] = CaesarCipher.decrypt(text, shift)
        return results


class TestCaesarBasic(unittest.TestCase):
    """Test basic encryption and decryption"""
    
    def test_encrypt_single_char(self):
        """Test encrypting a single character"""
        self.assertEqual(CaesarCipher.encrypt("A", 1), "B")
        self.assertEqual(CaesarCipher.encrypt("A", 3), "D")
        self.assertEqual(CaesarCipher.encrypt("a", 1), "b")
    
    def test_decrypt_single_char(self):
        """Test decrypting a single character"""
        self.assertEqual(CaesarCipher.decrypt("B", 1), "A")
        self.assertEqual(CaesarCipher.decrypt("D", 3), "A")
        self.assertEqual(CaesarCipher.decrypt("b", 1), "a")
    
    def test_encrypt_word(self):
        """Test encrypting a word"""
        self.assertEqual(CaesarCipher.encrypt("HELLO", 3), "KHOOR")
        self.assertEqual(CaesarCipher.encrypt("hello", 3), "khoor")
    
    def test_decrypt_word(self):
        """Test decrypting a word"""
        self.assertEqual(CaesarCipher.decrypt("KHOOR", 3), "HELLO")
        self.assertEqual(CaesarCipher.decrypt("khoor", 3), "hello")
    
    def test_encrypt_phrase(self):
        """Test encrypting a phrase"""
        message = "The quick brown fox"
        encrypted = CaesarCipher.encrypt(message, 5)
        decrypted = CaesarCipher.decrypt(encrypted, 5)
        self.assertEqual(decrypted, message)


class TestCaesarShifts(unittest.TestCase):
    """Test different shift values"""
    
    def test_shift_zero(self):
        """Test with shift 0 (no change)"""
        text = "HELLO"
        self.assertEqual(CaesarCipher.encrypt(text, 0), text)
    
    def test_shift_one(self):
        """Test with shift 1"""
        self.assertEqual(CaesarCipher.encrypt("ABC", 1), "BCD")
    
    def test_shift_thirteen(self):
        """Test ROT13 (shift 13)"""
        text = "HELLO"
        encrypted = CaesarCipher.encrypt(text, 13)
        # ROT13 applied twice should return original
        decrypted = CaesarCipher.encrypt(encrypted, 13)
        self.assertEqual(decrypted, text)
    
    def test_shift_twenty_five(self):
        """Test with maximum shift (25)"""
        encrypted = CaesarCipher.encrypt("ABC", 25)
        decrypted = CaesarCipher.decrypt(encrypted, 25)
        self.assertEqual(decrypted, "ABC")
    
    def test_negative_shift(self):
        """Test with negative shift"""
        text = "HELLO"
        encrypted = CaesarCipher.encrypt(text, 5)
        decrypted = CaesarCipher.encrypt(encrypted, -5)
        self.assertEqual(decrypted, text)
    
    def test_shift_wrapping(self):
        """Test that shift wraps around alphabet"""
        # Z with shift 1 should be A
        self.assertEqual(CaesarCipher.encrypt("Z", 1), "A")
        self.assertEqual(CaesarCipher.encrypt("z", 1), "a")
    
    def test_large_shift(self):
        """Test with shift larger than 26"""
        # Shift 27 should be same as shift 1
        encrypted1 = CaesarCipher.encrypt("ABC", 1)
        encrypted27 = CaesarCipher.encrypt("ABC", 27)
        self.assertEqual(encrypted1, encrypted27)


class TestCaesarCasePreservation(unittest.TestCase):
    """Test that case is preserved"""
    
    def test_uppercase_preserved(self):
        """Test that uppercase letters stay uppercase"""
        encrypted = CaesarCipher.encrypt("HELLO", 3)
        self.assertTrue(encrypted.isupper())
    
    def test_lowercase_preserved(self):
        """Test that lowercase letters stay lowercase"""
        encrypted = CaesarCipher.encrypt("hello", 3)
        self.assertTrue(encrypted.islower())
    
    def test_mixed_case_preserved(self):
        """Test that mixed case is preserved"""
        text = "Hello World"
        encrypted = CaesarCipher.encrypt(text, 5)
        # "Hello World" -> "Mjqqt Btwqi"
        self.assertEqual(encrypted[0], 'M')  # Capital H -> M
        self.assertEqual(encrypted[6], 'B')  # Capital W -> B
        self.assertTrue(encrypted[0].isupper())
        self.assertTrue(encrypted[6].isupper())
        # Check lowercase is preserved
        self.assertEqual(encrypted[1], 'j')  # lowercase e -> j
        self.assertTrue(encrypted[1].islower())


class TestCaesarNonAlphabetic(unittest.TestCase):
    """Test handling of non-alphabetic characters"""
    
    def test_numbers_preserved(self):
        """Test that numbers are preserved"""
        text = "Hello123"
        encrypted = CaesarCipher.encrypt(text, 5)
        self.assertTrue("123" in encrypted)
    
    def test_spaces_preserved(self):
        """Test that spaces are preserved"""
        text = "Hello World"
        encrypted = CaesarCipher.encrypt(text, 3)
        self.assertEqual(encrypted[5], " ")
    
    def test_punctuation_preserved(self):
        """Test that punctuation is preserved"""
        text = "Hello, World!"
        encrypted = CaesarCipher.encrypt(text, 3)
        # "Hello, World!" -> "Khoor, Zruog!"
        self.assertEqual(encrypted[5], ",")
        self.assertEqual(encrypted[12], "!")
    
    def test_special_characters_preserved(self):
        """Test that special characters are preserved"""
        text = "Price: $99.99"
        encrypted = CaesarCipher.encrypt(text, 3)
        self.assertTrue(":" in encrypted)
        self.assertTrue("$" in encrypted)
        self.assertTrue("." in encrypted)
    
    def test_all_non_alphabetic(self):
        """Test string with no alphabetic characters"""
        text = "123 !@# $%^"
        encrypted = CaesarCipher.encrypt(text, 5)
        self.assertEqual(encrypted, text)


class TestCaesarEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_empty_string(self):
        """Test encrypting empty string"""
        self.assertEqual(CaesarCipher.encrypt("", 5), "")
        self.assertEqual(CaesarCipher.decrypt("", 5), "")
    
    def test_single_character(self):
        """Test single character"""
        encrypted = CaesarCipher.encrypt("A", 3)
        self.assertEqual(encrypted, "D")
    
    def test_single_space(self):
        """Test single space"""
        self.assertEqual(CaesarCipher.encrypt(" ", 5), " ")
    
    def test_very_long_string(self):
        """Test with very long string"""
        text = "A" * 1000
        encrypted = CaesarCipher.encrypt(text, 3)
        decrypted = CaesarCipher.decrypt(encrypted, 3)
        self.assertEqual(decrypted, text)
    
    def test_all_vowels(self):
        """Test string with all vowels"""
        text = "aeiouAEIOU"
        encrypted = CaesarCipher.encrypt(text, 1)
        decrypted = CaesarCipher.decrypt(encrypted, 1)
        self.assertEqual(decrypted, text)
    
    def test_all_consonants(self):
        """Test string with all consonants"""
        text = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
        encrypted = CaesarCipher.encrypt(text, 1)
        decrypted = CaesarCipher.decrypt(encrypted, 1)
        self.assertEqual(decrypted, text)


class TestCaesarSymmetry(unittest.TestCase):
    """Test encryption/decryption symmetry"""
    
    def test_encrypt_decrypt_symmetry(self):
        """Test that decrypt(encrypt(x)) == x"""
        test_cases = [
            "Hello",
            "The quick brown fox",
            "UPPERCASE",
            "lowercase",
            "MiXeD CaSe",
            "With Numbers 123",
            "With! Special? Chars!",
        ]
        
        for text in test_cases:
            for shift in [1, 3, 5, 13, 25]:
                encrypted = CaesarCipher.encrypt(text, shift)
                decrypted = CaesarCipher.decrypt(encrypted, shift)
                self.assertEqual(decrypted, text, 
                    f"Failed for '{text}' with shift {shift}")
    
    def test_double_encryption_cancels(self):
        """Test that encrypt twice with same key cancels out"""
        text = "HELLO"
        encrypted1 = CaesarCipher.encrypt(text, 13)
        encrypted2 = CaesarCipher.encrypt(encrypted1, 13)
        self.assertEqual(encrypted2, text)  # ROT13 applied twice
    
    def test_encrypt_then_decrypt_shifts(self):
        """Test encrypt with shift5, then decrypt with shift5"""
        text = "ABCXYZ"
        encrypted = CaesarCipher.encrypt(text, 5)
        decrypted = CaesarCipher.decrypt(encrypted, 5)
        self.assertEqual(decrypted, text)


class TestCaesarBruteForce(unittest.TestCase):
    """Test brute force functionality"""
    
    def test_brute_force_returns_all_shifts(self):
        """Test that brute force returns all 25 shifts"""
        results = CaesarCipher.brute_force("KHOOR")
        self.assertEqual(len(results), 25)
        self.assertIn(1, results)
        self.assertIn(25, results)
    
    def test_brute_force_contains_original(self):
        """Test that brute force contains the correct decryption"""
        encrypted = "Khoor Zruog"
        results = CaesarCipher.brute_force(encrypted)
        # Should contain "Hello World" at shift 3
        self.assertIn("Hello World", results.values())
    
    def test_brute_force_all_unique(self):
        """Test that all brute force results are present"""
        results = CaesarCipher.brute_force("HELLO")
        self.assertEqual(len(results), 25)
        # All shifts 1-25 should be keys
        for shift in range(1, 26):
            self.assertIn(shift, results)
    
    def test_brute_force_preserves_non_alpha(self):
        """Test brute force with non-alphabetic characters"""
        encrypted = "Khoor, Zruog!"
        results = CaesarCipher.brute_force(encrypted)
        # Check that punctuation is preserved in results
        for decryption in results.values():
            self.assertIn(",", decryption)
            self.assertIn("!", decryption)


class TestCaesarRealWorldExamples(unittest.TestCase):
    """Test with real-world examples"""
    
    def test_famous_phrase(self):
        """Test with famous phrase"""
        original = "The quick brown fox jumps over the lazy dog"
        shift = 7
        encrypted = CaesarCipher.encrypt(original, shift)
        decrypted = CaesarCipher.decrypt(encrypted, shift)
        self.assertEqual(decrypted, original)
    
    def test_multiple_sentences(self):
        """Test with multiple sentences"""
        text = "Hello world. This is a test. How are you?"
        encrypted = CaesarCipher.encrypt(text, 5)
        decrypted = CaesarCipher.decrypt(encrypted, 5)
        self.assertEqual(decrypted, text)
    
    def test_email_format(self):
        """Test with email-like text"""
        text = "contact@example.com 123-456-7890"
        encrypted = CaesarCipher.encrypt(text, 3)
        decrypted = CaesarCipher.decrypt(encrypted, 3)
        self.assertEqual(decrypted, text)


class TestCaesarConsistency(unittest.TestCase):
    """Test consistency of operations"""
    
    def test_same_shift_same_result(self):
        """Test that same input with same shift produces same result"""
        text = "HELLO"
        result1 = CaesarCipher.encrypt(text, 3)
        result2 = CaesarCipher.encrypt(text, 3)
        self.assertEqual(result1, result2)
    
    def test_different_shifts_different_results(self):
        """Test that different shifts produce different results"""
        text = "HELLO"
        result1 = CaesarCipher.encrypt(text, 1)
        result2 = CaesarCipher.encrypt(text, 2)
        self.assertNotEqual(result1, result2)
    
    def test_shift_combinations(self):
        """Test that shift combinations work correctly"""
        text = "HELLO"
        # Encrypt with 3, then with 4 should equal encrypt with 7
        encrypted_3 = CaesarCipher.encrypt(text, 3)
        encrypted_7_after_3 = CaesarCipher.encrypt(encrypted_3, 4)
        encrypted_7 = CaesarCipher.encrypt(text, 7)
        self.assertEqual(encrypted_7_after_3, encrypted_7)


class TestCaesarInvalidInputHandling(unittest.TestCase):
    """Test handling of potentially invalid inputs"""
    
    def test_unicode_characters(self):
        """Test with unicode characters"""
        # Unicode characters should pass through unchanged
        text = "Hello™ World©"
        encrypted = CaesarCipher.encrypt(text, 3)
        # Non-ASCII should be preserved
        self.assertIn("™", encrypted)
        self.assertIn("©", encrypted)
    
    def test_tabs_and_newlines(self):
        """Test with tabs and newlines"""
        text = "Hello\tWorld\nTest"
        encrypted = CaesarCipher.encrypt(text, 5)
        decrypted = CaesarCipher.decrypt(encrypted, 5)
        self.assertEqual(decrypted, text)
    
    def test_repeated_characters(self):
        """Test with repeated characters"""
        text = "AAAA"
        encrypted = CaesarCipher.encrypt(text, 3)
        self.assertEqual(encrypted, "DDDD")
        self.assertEqual(len(encrypted), len(text))


class TestCaesarPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def test_performance_long_text(self):
        """Test that long text is handled efficiently"""
        # Create a long text
        text = "The quick brown fox jumps over the lazy dog. " * 100
        
        # Should complete without timeout
        encrypted = CaesarCipher.encrypt(text, 5)
        decrypted = CaesarCipher.decrypt(encrypted, 5)
        
        self.assertEqual(decrypted, text)
        self.assertEqual(len(encrypted), len(text))


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
