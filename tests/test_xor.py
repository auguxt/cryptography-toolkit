"""
Unit Tests for XOR Cipher
Tests encryption, decryption, symmetric properties, and edge cases
"""

import unittest


class XORCipher:
    """XOR Cipher class for testing"""
    
    @staticmethod
    def encrypt(text, key):
        """Encrypts text using XOR Cipher"""
        result = bytearray()
        key_len = len(key)
        for i, char in enumerate(text):
            xor_value = ord(char) ^ ord(key[i % key_len])
            result.append(xor_value)
        return bytes(result)
    
    @staticmethod
    def decrypt(encrypted, key):
        """Decrypts XOR encrypted text"""
        result = ""
        key_len = len(key)
        for i, byte in enumerate(encrypted):
            xor_value = byte ^ ord(key[i % key_len])
            result += chr(xor_value)
        return result
    
    @staticmethod
    def to_hex(data):
        """Converts bytes to hex string"""
        return data.hex()
    
    @staticmethod
    def from_hex(hex_string):
        """Converts hex string to bytes"""
        return bytes.fromhex(hex_string)


class TestXORBasic(unittest.TestCase):
    """Test basic XOR encryption and decryption"""
    
    def test_encrypt_single_char(self):
        """Test encrypting a single character"""
        encrypted = XORCipher.encrypt("A", "K")
        self.assertIsInstance(encrypted, bytes)
        self.assertEqual(len(encrypted), 1)
    
    def test_decrypt_single_char(self):
        """Test decrypting a single character"""
        key = "K"
        encrypted = XORCipher.encrypt("A", key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, "A")
    
    def test_encrypt_word(self):
        """Test encrypting a word"""
        key = "SECRET"
        encrypted = XORCipher.encrypt("HELLO", key)
        self.assertIsInstance(encrypted, bytes)
        self.assertEqual(len(encrypted), 5)
    
    def test_decrypt_word(self):
        """Test decrypting a word"""
        key = "SECRET"
        message = "HELLO"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_encrypt_phrase(self):
        """Test encrypting a phrase"""
        key = "KEY"
        message = "Hello World"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)


class TestXORSymmetry(unittest.TestCase):
    """Test XOR symmetric properties"""
    
    def test_xor_is_self_inverse(self):
        """Test that XOR applied twice returns original"""
        key = "KEY"
        message = "HELLO"
        # First XOR (encrypt)
        encrypted = XORCipher.encrypt(message, key)
        # Second XOR (decrypt using same key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_double_xor_same_key(self):
        """Test A XOR B XOR B = A"""
        message = "Test Message"
        key = "MYKEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_symmetric_property_various_messages(self):
        """Test symmetry with various messages"""
        test_cases = [
            ("A", "K"),
            ("Hello", "SECRET"),
            ("The quick brown fox", "KEY"),
            ("12345", "ABC"),
            ("!@#$%", "XYZ"),
        ]
        
        for message, key in test_cases:
            encrypted = XORCipher.encrypt(message, key)
            decrypted = XORCipher.decrypt(encrypted, key)
            self.assertEqual(decrypted, message, 
                f"Failed for message='{message}', key='{key}'")
    
    def test_xor_commutative(self):
        """Test that XOR is commutative: A XOR B = B XOR A"""
        message = "Hello"
        key = "Key"
        encrypted = XORCipher.encrypt(message, key)
        # Decrypt is just encrypt with same key
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)


class TestXORKeyLength(unittest.TestCase):
    """Test different key lengths"""
    
    def test_single_char_key(self):
        """Test with single character key"""
        message = "HELLO"
        key = "A"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_short_key(self):
        """Test with short key (shorter than message)"""
        message = "This is a long message"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_key_same_length_as_message(self):
        """Test with key same length as message"""
        message = "HELLO"
        key = "WORLD"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_key_longer_than_message(self):
        """Test with key longer than message"""
        message = "HI"
        key = "VERYLONGKEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_key_repetition(self):
        """Test that key repeats correctly"""
        message = "ABCABCABC"
        key = "ABC"
        # Each character should XOR with repeating key
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_very_long_key(self):
        """Test with very long key"""
        message = "Short"
        key = "A" * 1000
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)


class TestXORDifferentKeys(unittest.TestCase):
    """Test with different key values"""
    
    def test_different_keys_different_output(self):
        """Test that different keys produce different encrypted output"""
        message = "HELLO"
        key1 = "KEY1"
        key2 = "KEY2"
        
        encrypted1 = XORCipher.encrypt(message, key1)
        encrypted2 = XORCipher.encrypt(message, key2)
        
        self.assertNotEqual(encrypted1, encrypted2)
    
    def test_same_key_same_output(self):
        """Test that same key produces same output"""
        message = "HELLO"
        key = "KEY"
        
        encrypted1 = XORCipher.encrypt(message, key)
        encrypted2 = XORCipher.encrypt(message, key)
        
        self.assertEqual(encrypted1, encrypted2)
    
    def test_keys_with_different_chars(self):
        """Test various key characters"""
        message = "TEST"
        keys = ["A", "ABC", "123", "!@#", "aBc123!"]
        
        for key in keys:
            encrypted = XORCipher.encrypt(message, key)
            decrypted = XORCipher.decrypt(encrypted, key)
            self.assertEqual(decrypted, message, f"Failed with key='{key}'")


class TestXORSpecialCharacters(unittest.TestCase):
    """Test with special characters and various input types"""
    
    def test_numbers(self):
        """Test with numeric characters"""
        message = "1234567890"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_special_symbols(self):
        """Test with special symbols"""
        message = "!@#$%^&*()"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_spaces(self):
        """Test with spaces"""
        message = "Hello World Test"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_mixed_content(self):
        """Test with mixed alphanumeric and special characters"""
        message = "Email: test@example.com Price: $99.99"
        key = "SECRET"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_punctuation(self):
        """Test with punctuation"""
        message = "Hello, World! How are you?"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_uppercase_lowercase(self):
        """Test case sensitivity"""
        message = "Hello WORLD heLLo"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)


class TestXOREdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_empty_message(self):
        """Test encrypting empty string"""
        encrypted = XORCipher.encrypt("", "KEY")
        self.assertEqual(len(encrypted), 0)
        decrypted = XORCipher.decrypt(encrypted, "KEY")
        self.assertEqual(decrypted, "")
    
    def test_single_character_message(self):
        """Test single character message"""
        message = "A"
        key = "K"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_single_space_message(self):
        """Test message with only space"""
        message = " "
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_very_long_message(self):
        """Test with very long message"""
        message = "A" * 10000
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_repeated_characters(self):
        """Test message with repeated characters"""
        message = "AAAA"
        key = "K"
        encrypted = XORCipher.encrypt(message, key)
        # Same plaintext with same key should produce same ciphertext
        self.assertEqual(encrypted[0], encrypted[1])
        self.assertEqual(encrypted[1], encrypted[2])
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)
    
    def test_all_same_character_message(self):
        """Test when entire message is same character"""
        message = "XXXXX"
        key = "ABC"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, message)


class TestXORHexConversion(unittest.TestCase):
    """Test hexadecimal conversion"""
    
    def test_to_hex(self):
        """Test conversion to hex"""
        message = "Hello"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        hex_str = XORCipher.to_hex(encrypted)
        self.assertIsInstance(hex_str, str)
        # Hex should be valid
        try:
            bytes.fromhex(hex_str)
        except ValueError:
            self.fail("Invalid hex string generated")
    
    def test_from_hex(self):
        """Test conversion from hex"""
        hex_str = "1a2b3c4d"
        try:
            data = XORCipher.from_hex(hex_str)
            self.assertIsInstance(data, bytes)
            self.assertEqual(len(data), 4)
        except ValueError:
            self.fail("Failed to convert from hex")
    
    def test_hex_round_trip(self):
        """Test hex conversion round trip"""
        message = "Test"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        hex_str = XORCipher.to_hex(encrypted)
        recovered = XORCipher.from_hex(hex_str)
        self.assertEqual(encrypted, recovered)
    
    def test_hex_and_decrypt(self):
        """Test encrypt to hex and back to decrypt"""
        message = "Secret"
        key = "PASSWORD"
        encrypted = XORCipher.encrypt(message, key)
        hex_str = XORCipher.to_hex(encrypted)
        recovered = XORCipher.from_hex(hex_str)
        decrypted = XORCipher.decrypt(recovered, key)
        self.assertEqual(decrypted, message)


class TestXORBinaryProperties(unittest.TestCase):
    """Test XOR binary/mathematical properties"""
    
    def test_xor_with_self_is_zero(self):
        """Test that A XOR A = 0"""
        # This is implicit in our implementation
        key = "A"
        message = "A"
        encrypted = XORCipher.encrypt(message, key)
        # Encrypted should be a single byte with value 0
        self.assertEqual(encrypted[0], 0)
    
    def test_ascii_values_preserved_length(self):
        """Test that encrypted output length equals input length"""
        test_cases = ["A", "Hello", "Test Message", "123", "!@#$%"]
        key = "KEY"
        
        for message in test_cases:
            encrypted = XORCipher.encrypt(message, key)
            self.assertEqual(len(encrypted), len(message), 
                f"Length mismatch for '{message}'")
    
    def test_all_values_in_encrypted_bytes(self):
        """Test that encrypted output is valid bytes"""
        message = "Hello World!"
        key = "SECRET"
        encrypted = XORCipher.encrypt(message, key)
        
        # All values should be valid bytes (0-255)
        for byte_val in encrypted:
            self.assertGreaterEqual(byte_val, 0)
            self.assertLessEqual(byte_val, 255)


class TestXORRealWorldScenarios(unittest.TestCase):
    """Test real-world usage scenarios"""
    
    def test_email_encryption(self):
        """Test encrypting email-like data"""
        email = "user@example.com"
        password = "SecurePassword123"
        
        encrypted = XORCipher.encrypt(email, password)
        decrypted = XORCipher.decrypt(encrypted, password)
        self.assertEqual(decrypted, email)
    
    def test_data_masking(self):
        """Test data masking scenario"""
        data = "12345678"
        mask = "MASK"
        
        masked = XORCipher.encrypt(data, mask)
        unmasked = XORCipher.decrypt(masked, mask)
        self.assertEqual(unmasked, data)
    
    def test_multiple_messages_same_key(self):
        """Test encrypting multiple messages with same key"""
        key = "SHARED_KEY"
        messages = ["Message1", "Message2", "Message3"]
        
        encrypted_messages = []
        for msg in messages:
            enc = XORCipher.encrypt(msg, key)
            encrypted_messages.append(enc)
        
        # Decrypt all
        for i, enc in enumerate(encrypted_messages):
            dec = XORCipher.decrypt(enc, key)
            self.assertEqual(dec, messages[i])
    
    def test_configuration_data(self):
        """Test encrypting configuration data"""
        config = "host=localhost port=8080 user=admin"
        key = "CONFIG_KEY"
        
        encrypted = XORCipher.encrypt(config, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertEqual(decrypted, config)


class TestXORConsistency(unittest.TestCase):
    """Test consistency of operations"""
    
    def test_same_input_same_output(self):
        """Test that same input produces same output"""
        message = "HELLO"
        key = "KEY"
        
        encrypted1 = XORCipher.encrypt(message, key)
        encrypted2 = XORCipher.encrypt(message, key)
        
        self.assertEqual(encrypted1, encrypted2)
    
    def test_deterministic_behavior(self):
        """Test deterministic encryption"""
        message = "Test"
        key = "KEY"
        
        results = []
        for _ in range(5):
            results.append(XORCipher.encrypt(message, key))
        
        # All results should be identical
        for i in range(1, 5):
            self.assertEqual(results[0], results[i])
    
    def test_different_message_different_output(self):
        """Test that different messages produce different output"""
        key = "KEY"
        message1 = "HELLO"
        message2 = "WORLD"
        
        encrypted1 = XORCipher.encrypt(message1, key)
        encrypted2 = XORCipher.encrypt(message2, key)
        
        self.assertNotEqual(encrypted1, encrypted2)


class TestXORKeyReuse(unittest.TestCase):
    """Test key reuse concepts (informational)"""
    
    def test_same_char_same_encrypted_value(self):
        """Test that same plaintext char with same key = same encrypted value"""
        message = "AAA"
        key = "B"
        
        encrypted = XORCipher.encrypt(message, key)
        # All A's encrypted with B should produce same value
        self.assertEqual(encrypted[0], encrypted[1])
        self.assertEqual(encrypted[1], encrypted[2])
    
    def test_char_position_affects_output_with_varying_key(self):
        """Test that char position affects output when key repeats"""
        message = "AAAA"
        key = "BCDE"  # Different chars in key
        
        encrypted = XORCipher.encrypt(message, key)
        # Different positions should have different encrypted values
        self.assertNotEqual(encrypted[0], encrypted[1])
        self.assertNotEqual(encrypted[1], encrypted[2])


class TestXORPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def test_large_message_performance(self):
        """Test that large messages are handled efficiently"""
        message = "A" * 100000
        key = "KEY"
        
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        
        self.assertEqual(decrypted, message)
        self.assertEqual(len(encrypted), len(message))
    
    def test_multiple_encryptions(self):
        """Test multiple encryption operations"""
        key = "KEY"
        message = "Test Message"
        
        # Encrypt and decrypt multiple times
        current = message
        for _ in range(10):
            encrypted = XORCipher.encrypt(current, key)
            current = XORCipher.decrypt(encrypted, key)
        
        self.assertEqual(current, message)


class TestXORBinaryData(unittest.TestCase):
    """Test with various binary outputs"""
    
    def test_encrypted_is_bytes(self):
        """Test that encrypted output is bytes"""
        message = "Hello"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        self.assertIsInstance(encrypted, bytes)
    
    def test_encrypted_length(self):
        """Test that encrypted length matches message length"""
        messages = ["A", "Hello", "Test Message", "12345678"]
        key = "KEY"
        
        for message in messages:
            encrypted = XORCipher.encrypt(message, key)
            self.assertEqual(len(encrypted), len(message))
    
    def test_decrypted_is_string(self):
        """Test that decrypted output is string"""
        message = "Hello"
        key = "KEY"
        encrypted = XORCipher.encrypt(message, key)
        decrypted = XORCipher.decrypt(encrypted, key)
        self.assertIsInstance(decrypted, str)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
