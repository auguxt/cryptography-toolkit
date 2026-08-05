"""
Caesar Cipher - Usage Examples
Demonstrates how to use the caesar_cipher module in different scenarios
"""

# Import the cipher functions
# (In practice, you'd do: from caesar_cipher import encrypt, decrypt, brute_force)

# For this example, we'll define them inline
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


def decrypt(text, shift):
    """Decrypts text using Caesar Cipher"""
    return encrypt(text, -shift)


def brute_force(text):
    """Tries all possible Caesar Cipher shifts"""
    results = {}
    for shift in range(1, 26):
        results[shift] = decrypt(text, shift)
    return results


# ============================================================================
# EXAMPLE 1: Basic Encryption and Decryption
# ============================================================================
print("=" * 70)
print("EXAMPLE 1: Basic Encryption and Decryption")
print("=" * 70)

message = "The quick brown fox jumps over the lazy dog"
shift_key = 5

print(f"\nOriginal message: {message}")
print(f"Shift key:        {shift_key}")

encrypted = encrypt(message, shift_key)
print(f"Encrypted:        {encrypted}")

decrypted = decrypt(encrypted, shift_key)
print(f"Decrypted:        {decrypted}")
print(f"Match:            {'✓ YES' if decrypted == message else '✗ NO'}")


# ============================================================================
# EXAMPLE 2: Different Shift Values
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: Same Message with Different Shifts")
print("=" * 70)

message = "HELLO"
print(f"\nOriginal: {message}\n")

for shift in [1, 3, 7, 13, 25]:
    enc = encrypt(message, shift)
    print(f"Shift {shift:2d}: {enc}")


# ============================================================================
# EXAMPLE 3: Case Sensitivity
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 3: Preserving Case and Non-Alphabetic Characters")
print("=" * 70)

message = "Hello, World! 123"
shift_key = 3

print(f"\nOriginal:  {message}")
encrypted = encrypt(message, shift_key)
print(f"Encrypted: {encrypted}")
decrypted = decrypt(encrypted, shift_key)
print(f"Decrypted: {decrypted}")

print("\nNote: Numbers, punctuation, and spaces are preserved!")


# ============================================================================
# EXAMPLE 4: Brute Force Attack (Cracking Unknown Key)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 4: Brute Force Attack (Finding Unknown Key)")
print("=" * 70)

# Someone encrypted a message with unknown key
encrypted_message = "Khoor Zruog"
print(f"\nEncrypted message (unknown key): {encrypted_message}")
print("\nTrying all possible shifts:\n")

attempts = brute_force(encrypted_message)
for shift_val, decryption in attempts.items():
    # Highlight if it looks like English
    marker = " <- Makes sense!" if decryption.lower() in ["hello world"] else ""
    print(f"  Shift {shift_val:2d}: {decryption}{marker}")


# ============================================================================
# EXAMPLE 5: Frequency Analysis Hint
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 5: Common Sense Decryption")
print("=" * 70)

encrypted = "Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj"
print(f"\nEncrypted: {encrypted}")
print("\nBrute forcing...")

found = False
for shift in range(1, 26):
    decrypted = decrypt(encrypted, shift)
    if "the" in decrypted.lower():
        print(f"\n✓ Found at shift {shift}!")
        print(f"  Decrypted: {decrypted}")
        found = True
        break

if not found:
    print("✗ No common word 'the' found. Try analyzing character frequency!")


# ============================================================================
# EXAMPLE 6: ROT13 (Special Case: Shift 13)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 6: ROT13 (Shift 13 - Self-Inverse)")
print("=" * 70)

message = "The secret message"
rot13_encrypted = encrypt(message, 13)
rot13_decrypted = encrypt(rot13_encrypted, 13)  # Apply ROT13 twice = original

print(f"\nOriginal:           {message}")
print(f"After ROT13:        {rot13_encrypted}")
print(f"After ROT13 again:  {rot13_decrypted}")
print("\nNote: ROT13 is its own inverse! Applying it twice gives the original.")


# ============================================================================
# EXAMPLE 7: Practical Use Case - Simple Message Protection
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 7: Simple Message Protection")
print("=" * 70)

# Simulating a sender and receiver
sender_message = "Attack at dawn"
secret_key = 7

print(f"\n[SENDER] Original message: {sender_message}")
encrypted_msg = encrypt(sender_message, secret_key)
print(f"[SENDER] Encrypted with key {secret_key}: {encrypted_msg}")

print(f"\n[RECEIVER] Received: {encrypted_msg}")
print(f"[RECEIVER] Decrypting with key {secret_key}...")
decrypted_msg = decrypt(encrypted_msg, secret_key)
print(f"[RECEIVER] Decrypted: {decrypted_msg}")


# ============================================================================
# EXAMPLE 8: Security Weakness Demonstration
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 8: Why Caesar Cipher Is Insecure")
print("=" * 70)

encrypted = "Uryyb Jbeyq"
print(f"\nYou intercept: {encrypted}")
print("You don't know the shift key.\n")
print("But there are only 25 possible shifts!")
print("An attacker can try all of them in seconds:\n")

for shift in range(1, 26):
    result = decrypt(encrypted, shift)
    if shift <= 5 or shift >= 22:  # Show first and last few
        print(f"  Shift {shift:2d}: {result}")
    elif shift == 6:
        print("  ...")

print("\n✗ Caesar Cipher has only 25 possible keys (very weak!)")
print("✓ Modern encryption has billions of possible keys")


# ============================================================================
# EXAMPLE 9: Batch Encryption
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 9: Encrypting Multiple Messages")
print("=" * 70)

messages = [
    "Important data",
    "Secret password",
    "Confidential file"
]
key = 4

print(f"\nEncrypting {len(messages)} messages with key {key}:\n")

encrypted_messages = []
for msg in messages:
    enc = encrypt(msg, key)
    encrypted_messages.append(enc)
    print(f"  '{msg}' -> '{enc}'")

print(f"\nDecrypting all messages:\n")
for enc in encrypted_messages:
    dec = decrypt(enc, key)
    print(f"  '{enc}' -> '{dec}'")


# ============================================================================
# EXAMPLE 10: Educational - Character Mapping
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 10: Character Mapping (Shift 3)")
print("=" * 70)

print("\nAlphabet shifts with shift=3:")
print("\nOriginal: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
print("Shifted:  D E F G H I J K L M N O P Q R S T U V W X Y Z A B C")

print("\nExample: 'ABC' -> 'DEF'")
abc_test = encrypt("ABC", 3)
print(f"Result: {abc_test}")

print("\nExample: 'XYZ' -> 'ABC' (wraps around)")
xyz_test = encrypt("XYZ", 3)
print(f"Result: {xyz_test}")
