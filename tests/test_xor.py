# Tests for XOR Cipher

import unittest
from xor_cipher import encrypt, decrypt


class TestXOR(unittest.TestCase):

    def test_encrypt_then_decrypt(self):
        self.assertEqual(decrypt(encrypt("Hello", "KEY"), "KEY"), "Hello")

    def test_symmetric(self):
        # XOR applied twice = original
        message = "Test"
        key = "ABC"
        self.assertEqual(decrypt(encrypt(message, key), key), message)

    def test_different_keys_different_output(self):
        self.assertNotEqual(encrypt("HELLO", "KEY1"), encrypt("HELLO", "KEY2"))

    def test_same_key_same_output(self):
        self.assertEqual(encrypt("HELLO", "KEY"), encrypt("HELLO", "KEY"))

    def test_empty_string(self):
        self.assertEqual(decrypt(encrypt("", "KEY"), "KEY"), "")

    def test_special_characters(self):
        message = "Hello, World! 123"
        self.assertEqual(decrypt(encrypt(message, "KEY"), "KEY"), message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
