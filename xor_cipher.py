"""
Simple XOR Cipher Implementation
XOR each byte with a key (or repeating key) for encryption/decryption
"""

def encrypt(text, key):
    """
    Encrypts text using XOR Cipher
    
    Args:
        text (str): The text to encrypt
        key (str): The encryption key
    
    Returns:
        bytes: Encrypted text as bytes
    """
    result = bytearray()
    key_len = len(key)
    
    for i, char in enumerate(text):
        # XOR each character with corresponding key character (repeating)
        xor_value = ord(char) ^ ord(key[i % key_len])
        result.append(xor_value)
    
    return bytes(result)


def decrypt(encrypted, key):
    """
    Decrypts XOR encrypted text
    XOR is symmetric: A XOR B XOR B = A
    
    Args:
        encrypted (bytes): The encrypted bytes
        key (str): The decryption key (same as encryption key)
    
    Returns:
        str: Decrypted text
    """
    result = ""
    key_len = len(key)
    
    for i, byte in enumerate(encrypted):
        # XOR each byte with corresponding key character (repeating)
        xor_value = byte ^ ord(key[i % key_len])
        result += chr(xor_value)
    
    return result


def to_hex(data):
    """
    Converts bytes to hexadecimal string representation
    
    Args:
        data (bytes): The data to convert
    
    Returns:
        str: Hexadecimal string
    """
    return data.hex()


def from_hex(hex_string):
    """
    Converts hexadecimal string to bytes
    
    Args:
        hex_string (str): Hexadecimal string
    
    Returns:
        bytes: Converted bytes
    """
    return bytes.fromhex(hex_string)


# Example usage
if __name__ == "__main__":
    message = "Hello World"
    key = "SECRET"
    
    print("=" * 50)
    print("XOR CIPHER EXAMPLE")
    print("=" * 50)
    
    # Encrypt
    encrypted = encrypt(message, key)
    print(f"\nOriginal message: {message}")
    print(f"Encryption key:  {key}")
    print(f"Encrypted (hex): {to_hex(encrypted)}")
    print(f"Encrypted (raw): {encrypted}")
    
    # Decrypt
    decrypted = decrypt(encrypted, key)
    print(f"\nDecrypted:       {decrypted}")
    
    # Verify
    print(f"\nVerification: {'✓ PASS' if decrypted == message else '✗ FAIL'}")
    
    print("\n" + "=" * 50)
    print("HOW XOR WORKS")
    print("=" * 50)
    
    # Show character-by-character XOR process
    print(f"\nMessage: {message}")
    print(f"Key:     {key} (repeating)")
    print("\nCharacter-by-character breakdown:")
    
    key_len = len(key)
    for i in range(min(5, len(message))):
        char = message[i]
        key_char = key[i % key_len]
        xor_result = ord(char) ^ ord(key_char)
        print(f"  '{char}' XOR '{key_char}' = {ord(char):3d} XOR {ord(key_char):3d} = {xor_result:3d} (0x{xor_result:02x})")
    
    print("\n" + "=" * 50)
    print("MULTIPLE MESSAGES WITH SAME KEY")
    print("=" * 50)
    
    messages = ["Hello", "Secret", "Python"]
    key = "KEY"
    
    print(f"\nUsing key: '{key}'")
    for msg in messages:
        enc = encrypt(msg, key)
        dec = decrypt(enc, key)
        print(f"  '{msg}' -> {to_hex(enc)} -> '{dec}'")
