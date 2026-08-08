# Tests for RSA Cipher

import unittest
from rsa_cipher import generate_keys, encrypt, decrypt


class TestRSA(unittest.TestCase):

    def setUp(self):
        # Generate fresh keys before each test
        self.public_key, self.private_key = generate_keys()

    def test_encrypt_then_decrypt(self):
        message = "Hi"
        self.assertEqual(decrypt(encrypt(message, self.public_key), self.private_key), message)

    def test_encrypted_is_list(self):
        self.assertIsInstance(encrypt("A", self.public_key), list)

    def test_encrypted_length_matches_message(self):
        message = "Hello"
        self.assertEqual(len(encrypt(message, self.public_key)), len(message))

    def test_different_keys_generated(self):
        pub1, _ = generate_keys()
        pub2, _ = generate_keys()
        self.assertNotEqual(pub1, pub2)

    def test_various_messages(self):
        for message in ["A", "Hi", "Test"]:
            encrypted = encrypt(message, self.public_key)
            self.assertEqual(decrypt(encrypted, self.private_key), message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
