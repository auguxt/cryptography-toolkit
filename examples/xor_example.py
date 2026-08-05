"""
XOR Cipher - Usage Examples
Demonstrates how to use the XOR cipher module in different scenarios
"""

# Define XOR cipher functions inline for this example
def encrypt(text, key):
    """Encrypts text using XOR Cipher"""
    result = bytearray()
    key_len = len(key)
    for i, char in enumerate(text):
        xor_value = ord(char) ^ ord(key[i % key_len])
        result.append(xor_value)
    return bytes(result)


def decrypt(encrypted, key):
    """Decrypts XOR encrypted text (symmetric operation)"""
    result = ""
    key_len = len(key)
    for i, byte in enumerate(encrypted):
        xor_value = byte ^ ord(key[i % key_len])
        result += chr(xor_value)
    return result


def to_hex(data):
    """Converts bytes to hexadecimal string"""
    return data.hex()


def from_hex(hex_string):
    """Converts hexadecimal string to bytes"""
    return bytes.fromhex(hex_string)


def show_binary(text, key):
    """Shows binary representation of XOR operation"""
    print(f"\nBinary representation (first 3 chars):")
    key_len = len(key)
    for i in range(min(3, len(text))):
        char = text[i]
        key_char = key[i % key_len]
        xor_result = ord(char) ^ ord(key_char)
        print(f"  '{char}' {bin(ord(char))[2:].zfill(8)} XOR '{key_char}' {bin(ord(key_char))[2:].zfill(8)} = {bin(xor_result)[2:].zfill(8)} ({xor_result})")


# ============================================================================
# EXAMPLE 1: Basic Encryption and Decryption
# ============================================================================
print("=" * 70)
print("EXAMPLE 1: Basic XOR Encryption and Decryption")
print("=" * 70)

message = "Hello World"
key = "SECRET"

print(f"\nOriginal message: {message}")
print(f"Encryption key:  {key}")

encrypted = encrypt(message, key)
print(f"Encrypted (hex): {to_hex(encrypted)}")

decrypted = decrypt(encrypted, key)
print(f"Decrypted:       {decrypted}")
print(f"Match:           {'✓ YES' if decrypted == message else '✗ NO'}")


# ============================================================================
# EXAMPLE 2: Symmetric Property of XOR
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: XOR is Symmetric (A XOR B XOR B = A)")
print("=" * 70)

message = "Test"
key = "KEY"

print(f"\nOriginal: {message}")

# First XOR (encryption)
encrypted = encrypt(message, key)
print(f"After 1st XOR with key: {encrypted}")

# Second XOR (decryption) - same operation
decrypted = decrypt(encrypted, key)
print(f"After 2nd XOR with key: {decrypted}")

print("\n✓ Applying XOR twice with the same key returns the original!")
print("  This makes XOR both encryption and decryption method")


# ============================================================================
# EXAMPLE 3: Different Keys Produce Different Results
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 3: Different Keys Produce Different Encrypted Output")
print("=" * 70)

message = "HELLO"
print(f"\nMessage: {message}\n")

keys = ["A", "SECRET", "KEY", "X"]
for k in keys:
    enc = encrypt(message, k)
    print(f"Key '{k:8s}': {to_hex(enc)}")


# ============================================================================
# EXAMPLE 4: Binary Representation
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 4: Binary Representation of XOR Operation")
print("=" * 70)

message = "HI"
key = "K"

print(f"\nMessage: {message}")
print(f"Key:     {key}")

show_binary(message, key)

print(f"\nEncrypted (hex): {to_hex(encrypt(message, key))}")


# ============================================================================
# EXAMPLE 5: Key Length and Repetition
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 5: Key Repetition with Different Length Messages")
print("=" * 70)

key = "ABC"
messages = ["A", "ABCABC", "ABCABCABC", "ABCABCABCD"]

print(f"\nUsing key: '{key}' (3 characters)")
print("\nHow the key repeats:")

for msg in messages:
    key_usage = "".join([key[i % len(key)] for i in range(len(msg))])
    print(f"  Message '{msg}' uses key '{key_usage}'")


# ============================================================================
# EXAMPLE 6: The One-Time Pad Concept
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 6: One-Time Pad (Theoretically Unbreakable)")
print("=" * 70)

message = "SECRET"
random_key = "XYZABC"  # Key as long as message, random

print(f"\nMessage:  {message}")
print(f"One-time key (same length): {random_key}")

encrypted = encrypt(message, random_key)
print(f"Encrypted: {to_hex(encrypted)}")

print("\n✓ If key is:")
print("  - Random")
print("  - Same length as message")
print("  - Used only once")
print("  Then XOR is theoretically unbreakable (One-Time Pad)!")

print("\n✗ BUT in practice:")
print("  - Key reuse is vulnerable")
print("  - Key must be securely transmitted")
print("  - Managing huge random keys is impractical")


# ============================================================================
# EXAMPLE 7: Short Key Vulnerability (Key Reuse)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 7: Vulnerability - Reusing Short Keys")
print("=" * 70)

key = "KEY"
message1 = "secret message one"
message2 = "confidential data two"

enc1 = encrypt(message1, key)
enc2 = encrypt(message2, key)

print(f"\nKey:           {key}")
print(f"Message 1:     {message1}")
print(f"Encrypted 1:   {to_hex(enc1)}")
print(f"\nMessage 2:     {message2}")
print(f"Encrypted 2:   {to_hex(enc2)}")

print("\n⚠ WARNING: Using same short key for multiple messages is INSECURE!")
print("  Attackers can XOR the two ciphertexts:")
print(f"  {to_hex(enc1)} XOR {to_hex(enc2)}")
print("  This removes the key and reveals patterns!")

# Demonstrate the vulnerability
enc1_bytes = enc1
enc2_bytes = enc2
xor_result = bytes(a ^ b for a, b in zip(enc1_bytes, enc2_bytes))
print(f"\n  Result: {to_hex(xor_result)}")
print("  The attacker can analyze this to break the cipher!")


# ============================================================================
# EXAMPLE 8: Practical Use Case - Simple Data Masking
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 8: Practical Use Case - Data Masking")
print("=" * 70)

data = "12345678"
mask_key = "MASK"

print(f"\nOriginal data:  {data}")
masked = encrypt(data, mask_key)
print(f"Masked data:    {to_hex(masked)}")

unmasked = decrypt(masked, mask_key)
print(f"Unmasked data:  {unmasked}")

print("\n✓ Useful for obfuscating data temporarily")
print("✗ Not suitable for long-term security")


# ============================================================================
# EXAMPLE 9: Case Sensitivity and Special Characters
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 9: XOR Works with Any Characters")
print("=" * 70)

test_strings = [
    "Hello, World!",
    "email@example.com",
    "Price: $99.99",
    "Date: 2024-01-15"
]

key = "KEY"

print(f"\nUsing key: '{key}'\n")

for text in test_strings:
    enc = encrypt(text, key)
    dec = decrypt(enc, key)
    match = "✓" if dec == text else "✗"
    print(f"{match} '{text}' -> {to_hex(enc)} -> '{dec}'")


# ============================================================================
# EXAMPLE 10: Batch Encryption
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 10: Encrypting Multiple Messages")
print("=" * 70)

messages = [
    "Message 1",
    "Message 2",
    "Message 3"
]
key = "SHARED_KEY"

print(f"\nKey: '{key}'")
print(f"Encrypting {len(messages)} messages:\n")

encrypted_messages = []
for msg in messages:
    enc = encrypt(msg, key)
    encrypted_messages.append(enc)
    print(f"  '{msg}' -> {to_hex(enc)}")

print(f"\nDecrypting all messages:\n")
for enc in encrypted_messages:
    dec = decrypt(enc, key)
    print(f"  {to_hex(enc)} -> '{dec}'")


# ============================================================================
# EXAMPLE 11: XOR with Numbers
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 11: XOR with Numeric Content")
print("=" * 70)

numbers = "123456789"
key = "NUMERIC"

print(f"\nMessage:  {numbers}")
print(f"Key:      {key}")

encrypted = encrypt(numbers, key)
decrypted = decrypt(encrypted, key)

print(f"Encrypted: {to_hex(encrypted)}")
print(f"Decrypted: {decrypted}")
print(f"Match:     {'✓ YES' if decrypted == numbers else '✗ NO'}")


# ============================================================================
# EXAMPLE 12: Security Comparison
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 12: Security Comparison - XOR vs Caesar Cipher")
print("=" * 70)

message = "SECRET"

print(f"\nMessage: {message}\n")

print("Caesar Cipher (Shift 3):")
caesar_enc = "".join(chr((ord(c) - ord('A') + 3) % 26 + ord('A')) if c.isupper() 
                      else chr((ord(c) - ord('a') + 3) % 26 + ord('a')) if c.isalpha() 
                      else c for c in message)
print(f"  Encrypted: {caesar_enc}")
print(f"  Key space: 25 (only 25 possible keys)")
print(f"  Time to crack: < 1 second (brute force)")

print("\nXOR Cipher (Key 'MYKEY'):")
xor_enc = encrypt(message, "MYKEY")
print(f"  Encrypted: {to_hex(xor_enc)}")
print(f"  Key space: 2^(key_length * 8)")
print(f"  Time to crack: Depends on key length and randomness")

print("\nComparison:")
print("  Caesar: Fixed 25 possibilities - VERY WEAK")
print("  XOR:    Variable key length - STRONGER but still weak with reuse")
print("  Modern: AES, RSA, etc. - CRYPTOGRAPHICALLY SECURE")


# ============================================================================
# EXAMPLE 13: Text to Hex and Back
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 13: Hex Conversion")
print("=" * 70)

message = "Hello"
key = "XOR"

encrypted = encrypt(message, key)
hex_encrypted = to_hex(encrypted)

print(f"\nOriginal:        {message}")
print(f"Key:             {key}")
print(f"Encrypted:       {encrypted}")
print(f"As Hex:          {hex_encrypted}")
print(f"Hex reversed:    {from_hex(hex_encrypted)}")
print(f"Decrypted:       {decrypt(from_hex(hex_encrypted), key)}")


# ============================================================================
# EXAMPLE 14: Key Length Impact
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 14: Key Length Impact on Security")
print("=" * 70)

message = "Attack at noon"

print(f"\nMessage: {message} ({len(message)} chars)\n")

key_lengths = [1, 3, 7, 14]

for key_len in key_lengths:
    key = "A" * key_len
    encrypted = encrypt(message, key)
    print(f"Key length {key_len:2d} ('{key}'): {to_hex(encrypted)}")
    
print("\n✓ Longer keys (especially same length as message) are more secure")
print("✗ Single character key is weakest (pattern repeats every char)")
print("✓ Random key same length as message = One-Time Pad (unbreakable)")
