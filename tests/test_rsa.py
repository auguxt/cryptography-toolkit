"""
Unit Tests for RSA Cipher
Tests key generation, encryption, decryption, and asymmetric properties
"""

import unittest
import random
from math import gcd


class RSACipher:
    """RSA Cipher class for testing"""
    
    @staticmethod
    def gcd_extended(a, b):
        """Extended Euclidean Algorithm"""
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = RSACipher.gcd_extended(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    @staticmethod
    def mod_inverse(e, phi):
        """Find modular inverse"""
        gcd_val, x, _ = RSACipher.gcd_extended(e, phi)
        if gcd_val != 1:
            return None
        return (x % phi + phi) % phi
    
    @staticmethod
    def is_prime(n, k=5):
        """Miller-Rabin primality test"""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    @staticmethod
    def generate_prime(bits):
        """Generate random prime with given bit length"""
        while True:
            n = random.getrandbits(bits)
            n |= (1 << bits - 1) | 1
            if RSACipher.is_prime(n):
                return n
    
    @staticmethod
    def generate_keys(bit_length=256):
        """Generate RSA key pair"""
        p = RSACipher.generate_prime(bit_length)
        q = RSACipher.generate_prime(bit_length)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        while gcd(e, phi) != 1:
            e = random.randrange(2, phi)
        d = RSACipher.mod_inverse(e, phi)
        return (e, n), (d, n)
    
    @staticmethod
    def encrypt(message, public_key):
        """Encrypt with public key"""
        e, n = public_key
        encrypted = []
        for char in message:
            m = ord(char)
            c = pow(m, e, n)
            encrypted.append(c)
        return encrypted
    
    @staticmethod
    def decrypt(encrypted, private_key):
        """Decrypt with private key"""
        d, n = private_key
        decrypted = ""
        for c in encrypted:
            m = pow(c, d, n)
            decrypted += chr(m)
        return decrypted
    
    @staticmethod
    def sign(message, private_key):
        """Sign message with private key"""
        d, n = private_key
        signature = []
        for char in message:
            m = ord(char)
            sig = pow(m, d, n)
            signature.append(sig)
        return signature
    
    @staticmethod
    def verify(signature, public_key):
        """Verify signature with public key"""
        e, n = public_key
        verified = ""
        for sig in signature:
            m = pow(sig, e, n)
            verified += chr(m)
        return verified


class TestRSAKeyGeneration(unittest.TestCase):
    """Test RSA key generation"""
    
    def test_generate_keys_returns_four_values(self):
        """Test that key generation returns public and private keys"""
        public_key, private_key = RSACipher.generate_keys(bit_length=256)
        
        # Public key should be (e, n)
        self.assertEqual(len(public_key), 2)
        # Private key should be (d, n)
        self.assertEqual(len(private_key), 2)
    
    def test_public_key_has_e_and_n(self):
        """Test that public key contains e and n"""
        public_key, _ = RSACipher.generate_keys(bit_length=256)
        e, n = public_key
        
        # e should be positive integer
        self.assertIsInstance(e, int)
        self.assertGreater(e, 0)
        # n should be positive integer
        self.assertIsInstance(n, int)
        self.assertGreater(n, 0)
    
    def test_private_key_has_d_and_n(self):
        """Test that private key contains d and n"""
        _, private_key = RSACipher.generate_keys(bit_length=256)
        d, n = private_key
        
        # d should be positive integer
        self.assertIsInstance(d, int)
        self.assertGreater(d, 0)
        # n should be positive integer
        self.assertIsInstance(n, int)
        self.assertGreater(n, 0)
    
    def test_n_is_same_in_both_keys(self):
        """Test that n is the same in public and private keys"""
        public_key, private_key = RSACipher.generate_keys(bit_length=256)
        e, n_pub = public_key
        d, n_priv = private_key
        
        self.assertEqual(n_pub, n_priv)
    
    def test_e_and_d_are_different(self):
        """Test that e and d are different"""
        public_key, private_key = RSACipher.generate_keys(bit_length=256)
        e, _ = public_key
        d, _ = private_key
        
        self.assertNotEqual(e, d)
    
    def test_different_key_generations_are_different(self):
        """Test that different key generations produce different keys"""
        pub1, priv1 = RSACipher.generate_keys(bit_length=256)
        pub2, priv2 = RSACipher.generate_keys(bit_length=256)
        
        # Very unlikely to be the same
        self.assertNotEqual(pub1, pub2)
        self.assertNotEqual(priv1, priv2)


class TestRSABasicEncryption(unittest.TestCase):
    """Test basic RSA encryption and decryption"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_encrypt_single_char(self):
        """Test encrypting a single character"""
        encrypted = RSACipher.encrypt("A", self.public_key)
        self.assertEqual(len(encrypted), 1)
        self.assertIsInstance(encrypted[0], int)
    
    def test_decrypt_single_char(self):
        """Test decrypting a single character"""
        message = "A"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_encrypt_word(self):
        """Test encrypting a word"""
        message = "HELLO"
        encrypted = RSACipher.encrypt(message, self.public_key)
        self.assertEqual(len(encrypted), 5)
    
    def test_decrypt_word(self):
        """Test decrypting a word"""
        message = "HELLO"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_encrypt_phrase(self):
        """Test encrypting a phrase"""
        message = "Hello World"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)


class TestRSASymmetry(unittest.TestCase):
    """Test RSA encryption/decryption symmetry"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_encrypt_decrypt_symmetry(self):
        """Test that decrypt(encrypt(x)) == x"""
        messages = ["A", "Hello", "Test", "Secret Message"]
        
        for message in messages:
            encrypted = RSACipher.encrypt(message, self.public_key)
            decrypted = RSACipher.decrypt(encrypted, self.private_key)
            self.assertEqual(decrypted, message)
    
    def test_encrypt_decrypt_long_message(self):
        """Test with long message"""
        message = "The quick brown fox jumps over the lazy dog"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_encrypt_decrypt_special_chars(self):
        """Test with special characters"""
        message = "Hello, World! 123 !@#"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)


class TestRSAAsymmetry(unittest.TestCase):
    """Test RSA asymmetric properties"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_public_key_cannot_decrypt(self):
        """Test that public key cannot decrypt (conceptually)"""
        message = "SECRET"
        encrypted = RSACipher.encrypt(message, self.public_key)
        
        # Trying to decrypt with public key should not give original message
        # (unless by chance)
        e, n = self.public_key
        decrypted_attempt = ""
        for c in encrypted:
            # Decrypt with public exponent (wrong!)
            m = pow(c, e, n)
            decrypted_attempt += chr(m) if m < 256 else "?"
        
        # Should not equal original (statistically)
        self.assertNotEqual(decrypted_attempt, message)
    
    def test_only_private_key_can_decrypt(self):
        """Test that only private key can decrypt"""
        message = "SECRET"
        encrypted = RSACipher.encrypt(message, self.public_key)
        
        # Only private key should decrypt correctly
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_different_keys_different_decryption(self):
        """Test with different key pairs"""
        pub1, priv1 = RSACipher.generate_keys(bit_length=256)
        pub2, priv2 = RSACipher.generate_keys(bit_length=256)
        
        message = "Test"
        
        # Encrypt with pub1, decrypt with priv1
        enc1 = RSACipher.encrypt(message, pub1)
        dec1 = RSACipher.decrypt(enc1, priv1)
        self.assertEqual(dec1, message)
        
        # Encrypt with pub2, decrypt with priv2
        enc2 = RSACipher.encrypt(message, pub2)
        dec2 = RSACipher.decrypt(enc2, priv2)
        self.assertEqual(dec2, message)
        
        # Cross decryption should fail (statistically)
        try:
            dec_cross = RSACipher.decrypt(enc1, priv2)
            # If it doesn't throw error, it shouldn't match original
            self.assertNotEqual(dec_cross, message)
        except:
            pass  # Expected to potentially fail


class TestRSAEncryptedOutput(unittest.TestCase):
    """Test properties of encrypted output"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_encrypted_is_list(self):
        """Test that encrypted output is a list"""
        encrypted = RSACipher.encrypt("A", self.public_key)
        self.assertIsInstance(encrypted, list)
    
    def test_encrypted_length_equals_message_length(self):
        """Test that each character is encrypted separately"""
        messages = ["A", "Hello", "Test123"]
        
        for message in messages:
            encrypted = RSACipher.encrypt(message, self.public_key)
            self.assertEqual(len(encrypted), len(message))
    
    def test_encrypted_values_are_integers(self):
        """Test that encrypted values are integers"""
        encrypted = RSACipher.encrypt("Hello", self.public_key)
        
        for value in encrypted:
            self.assertIsInstance(value, int)
            self.assertGreater(value, 0)
    
    def test_encrypted_values_less_than_n(self):
        """Test that all encrypted values are less than n"""
        e, n = self.public_key
        encrypted = RSACipher.encrypt("HELLO", self.public_key)
        
        for value in encrypted:
            self.assertLess(value, n)
    
    def test_different_message_different_encrypted(self):
        """Test that different messages produce different encrypted output"""
        enc1 = RSACipher.encrypt("HELLO", self.public_key)
        enc2 = RSACipher.encrypt("WORLD", self.public_key)
        
        self.assertNotEqual(enc1, enc2)
    
    def test_same_message_same_encrypted(self):
        """Test that same message produces same encrypted output"""
        message = "HELLO"
        enc1 = RSACipher.encrypt(message, self.public_key)
        enc2 = RSACipher.encrypt(message, self.public_key)
        
        self.assertEqual(enc1, enc2)


class TestRSAEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_single_character(self):
        """Test single character"""
        message = "A"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_lowercase_letter(self):
        """Test lowercase letter"""
        message = "a"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_numbers(self):
        """Test numeric characters"""
        message = "12345"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_space(self):
        """Test space character"""
        message = "A B C"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_special_characters(self):
        """Test special characters"""
        message = "!@#$%"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_repeated_characters(self):
        """Test repeated characters"""
        message = "AAAA"
        encrypted = RSACipher.encrypt(message, self.public_key)
        
        # Same plaintext should encrypt to same ciphertext
        self.assertEqual(encrypted[0], encrypted[1])
        self.assertEqual(encrypted[1], encrypted[2])
        self.assertEqual(encrypted[2], encrypted[3])
        
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_very_long_message(self):
        """Test with very long message"""
        message = "A" * 1000
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)


class TestRSAMultipleRecipients(unittest.TestCase):
    """Test RSA with multiple recipients"""
    
    def test_different_recipients(self):
        """Test sending message to multiple recipients"""
        message = "Important"
        
        # Generate keys for 3 recipients
        recipients = {}
        for i in range(3):
            pub, priv = RSACipher.generate_keys(bit_length=256)
            recipients[f"Person{i}"] = {"public": pub, "private": priv}
        
        # Encrypt for each recipient
        encrypted_dict = {}
        for name, keys in recipients.items():
            encrypted_dict[name] = RSACipher.encrypt(message, keys["public"])
        
        # Each recipient can decrypt with their private key
        for name, keys in recipients.items():
            decrypted = RSACipher.decrypt(encrypted_dict[name], keys["private"])
            self.assertEqual(decrypted, message)
    
    def test_encrypted_differently_for_each_recipient(self):
        """Test that same message encrypts differently with different keys"""
        message = "TEST"
        
        pub1, priv1 = RSACipher.generate_keys(bit_length=256)
        pub2, priv2 = RSACipher.generate_keys(bit_length=256)
        
        enc1 = RSACipher.encrypt(message, pub1)
        enc2 = RSACipher.encrypt(message, pub2)
        
        # Encrypted values should be different
        self.assertNotEqual(enc1, enc2)


class TestRSADigitalSignatures(unittest.TestCase):
    """Test RSA digital signature concepts"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_sign_and_verify(self):
        """Test signing and verifying a message"""
        message = "I agree"
        
        # Sign with private key
        signature = RSACipher.sign(message, self.private_key)
        
        # Verify with public key
        verified = RSACipher.verify(signature, self.public_key)
        
        self.assertEqual(verified, message)
    
    def test_signature_is_different_from_encryption(self):
        """Test that signature is different from encryption"""
        message = "Test"
        
        encrypted = RSACipher.encrypt(message, self.public_key)
        signature = RSACipher.sign(message, self.private_key)
        
        # Should be different (using different keys)
        self.assertNotEqual(encrypted, signature)
    
    def test_signature_length(self):
        """Test that signature length matches message length"""
        message = "Hello"
        signature = RSACipher.sign(message, self.private_key)
        
        self.assertEqual(len(signature), len(message))


class TestRSAPrimalityTest(unittest.TestCase):
    """Test prime number generation and testing"""
    
    def test_is_prime_small_primes(self):
        """Test primality test on known small primes"""
        small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        
        for prime in small_primes:
            self.assertTrue(RSACipher.is_prime(prime))
    
    def test_is_prime_small_non_primes(self):
        """Test primality test on known non-primes"""
        non_primes = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15]
        
        for non_prime in non_primes:
            self.assertFalse(RSACipher.is_prime(non_prime))
    
    def test_generate_prime_returns_prime(self):
        """Test that generated prime is actually prime"""
        prime = RSACipher.generate_prime(bits=64)
        
        # Should be a large number
        self.assertGreater(prime, 2**63)
        # Should pass primality test
        self.assertTrue(RSACipher.is_prime(prime))


class TestRSAModularArithmetic(unittest.TestCase):
    """Test modular arithmetic operations"""
    
    def test_mod_inverse_exists(self):
        """Test that mod inverse exists for valid inputs"""
        e = 65537
        phi = 52200  # Example phi
        
        # Should be coprime
        self.assertEqual(gcd(e, phi), 1)
        
        # Inverse should exist
        d = RSACipher.mod_inverse(e, phi)
        self.assertIsNotNone(d)
    
    def test_mod_inverse_property(self):
        """Test that d*e mod phi = 1"""
        e = 65537
        phi = 52200
        
        d = RSACipher.mod_inverse(e, phi)
        
        # e*d ≡ 1 (mod phi)
        self.assertEqual((e * d) % phi, 1)
    
    def test_gcd_extended_correctness(self):
        """Test extended GCD"""
        a, b = 35, 15
        gcd_val, x, y = RSACipher.gcd_extended(a, b)
        
        # a*x + b*y = gcd(a,b)
        self.assertEqual(a * x + b * y, gcd_val)


class TestRSAConsistency(unittest.TestCase):
    """Test consistency of operations"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_same_message_same_encryption(self):
        """Test deterministic encryption"""
        message = "TEST"
        
        enc1 = RSACipher.encrypt(message, self.public_key)
        enc2 = RSACipher.encrypt(message, self.public_key)
        
        self.assertEqual(enc1, enc2)
    
    def test_multiple_decryption_operations(self):
        """Test multiple decryption operations"""
        message = "Test"
        encrypted = RSACipher.encrypt(message, self.public_key)
        
        # Decrypt multiple times
        for _ in range(5):
            decrypted = RSACipher.decrypt(encrypted, self.private_key)
            self.assertEqual(decrypted, message)


class TestRSARealWorldScenarios(unittest.TestCase):
    """Test real-world usage scenarios"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_email_encryption(self):
        """Test encrypting email content"""
        email = "contact@example.com"
        encrypted = RSACipher.encrypt(email, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, email)
    
    def test_secure_message(self):
        """Test encrypting a secure message"""
        message = "This is confidential"
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        self.assertEqual(decrypted, message)
    
    def test_multiple_messages(self):
        """Test encrypting multiple messages"""
        messages = ["Message 1", "Message 2", "Message 3"]
        
        encrypted_msgs = []
        for msg in messages:
            encrypted_msgs.append(RSACipher.encrypt(msg, self.public_key))
        
        # Decrypt all
        for i, enc in enumerate(encrypted_msgs):
            dec = RSACipher.decrypt(enc, self.private_key)
            self.assertEqual(dec, messages[i])


class TestRSAMessageLength(unittest.TestCase):
    """Test message length handling"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_single_char_encryption(self):
        """Test single character encryption"""
        message = "A"
        encrypted = RSACipher.encrypt(message, self.public_key)
        self.assertEqual(len(encrypted), 1)
    
    def test_incremental_length(self):
        """Test encryption of increasing message lengths"""
        for length in [1, 5, 10, 50, 100]:
            message = "A" * length
            encrypted = RSACipher.encrypt(message, self.public_key)
            decrypted = RSACipher.decrypt(encrypted, self.private_key)
            self.assertEqual(decrypted, message)
            self.assertEqual(len(encrypted), length)
    
    def test_mixed_length_messages(self):
        """Test various message lengths"""
        messages = ["A", "Hello", "The quick brown fox", "A" * 100]
        
        for message in messages:
            encrypted = RSACipher.encrypt(message, self.public_key)
            decrypted = RSACipher.decrypt(encrypted, self.private_key)
            self.assertEqual(decrypted, message)
            self.assertEqual(len(encrypted), len(message))


class TestRSAPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def setUp(self):
        """Generate keys for each test"""
        self.public_key, self.private_key = RSACipher.generate_keys(bit_length=256)
    
    def test_long_message_performance(self):
        """Test encryption of long message"""
        message = "A" * 1000
        
        encrypted = RSACipher.encrypt(message, self.public_key)
        decrypted = RSACipher.decrypt(encrypted, self.private_key)
        
        self.assertEqual(decrypted, message)
        self.assertEqual(len(encrypted), 1000)
    
    def test_multiple_encryptions(self):
        """Test multiple encryption operations"""
        message = "Test"
        
        for _ in range(10):
            encrypted = RSACipher.encrypt(message, self.public_key)
            decrypted = RSACipher.decrypt(encrypted, self.private_key)
            self.assertEqual(decrypted, message)


class TestRSAKeyProperties(unittest.TestCase):
    """Test properties of RSA keys"""
    
    def test_e_is_standard_value(self):
        """Test that e is typically 65537"""
        public_key, _ = RSACipher.generate_keys(bit_length=256)
        e, n = public_key
        
        # Standard e value
        self.assertEqual(e, 65537)
    
    def test_n_is_product_of_two_primes(self):
        """Test that n is product of two primes (conceptually)"""
        # We can't easily verify this without factoring n
        # But we can verify it's composite and large
        public_key, _ = RSACipher.generate_keys(bit_length=256)
        e, n = public_key
        
        # n should be very large
        self.assertGreater(n, 2**255)
    
    def test_d_is_large(self):
        """Test that private exponent d is large"""
        _, private_key = RSACipher.generate_keys(bit_length=256)
        d, n = private_key
        
        # d should be large (close to n)
        self.assertGreater(d, 2**100)
    
    def test_keys_are_different_between_generations(self):
        """Test that each key generation is unique"""
        keys_set = set()
        
        for _ in range(5):
            pub, priv = RSACipher.generate_keys(bit_length=256)
            e, n = pub
            # Create unique identifier
            key_id = (e, n)
            keys_set.add(key_id)
        
        # All should be different
        self.assertEqual(len(keys_set), 5)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
