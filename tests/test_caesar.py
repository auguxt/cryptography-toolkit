# Tests for Caesar Cipher

import unittest
from caesar_cipher import encrypt, decrypt, brute_force


class TestCaesar(unittest.TestCase):

    def test_encrypt(self):
        self.assertEqual(encrypt("HELLO", 3), "KHOOR")

    def test_decrypt(self):
        self.assertEqual(decrypt("KHOOR", 3), "HELLO")

    def test_encrypt_then_decrypt(self):
        self.assertEqual(decrypt(encrypt("Hello World", 5), 5), "Hello World")

    def test_keeps_spaces_and_symbols(self):
        self.assertEqual(encrypt("Hi, 123!", 3), "Kl, 123!")

    def test_wraps_around(self):
        self.assertEqual(encrypt("Z", 1), "A")

    def test_empty_string(self):
        self.assertEqual(encrypt("", 3), "")

    def test_brute_force_runs(self):
        # Just make sure it doesn't crash
        brute_force("Khoor Zruog")


if __name__ == "__main__":
    unittest.main(verbosity=2)
