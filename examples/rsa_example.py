"""
RSA Cipher - Usage Examples
Demonstrates how to use RSA cipher in different scenarios
"""

import random
from math import gcd


def gcd_extended(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(e, phi):
    """Find modular inverse"""
    gcd_val, x, _ = gcd_extended(e, phi)
    if gcd_val != 1:
        return None
    return (x % phi + phi) % phi


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


def generate_prime(bits):
    """Generate random prime with given bit length"""
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1
        if is_prime(n):
            return n


def generate_keys(bit_length=512):
    """Generate RSA key pair"""
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)


def encrypt(message, public_key):
    """Encrypt with public key"""
    e, n = public_key
    encrypted = []
    for char in message:
        m = ord(char)
        c = pow(m, e, n)
        encrypted.append(c)
    return encrypted


def decrypt(encrypted, private_key):
    """Decrypt with private key"""
    d, n = private_key
    decrypted = ""
    for c in encrypted:
        m = pow(c, d, n)
        decrypted += chr(m)
    return decrypted


def encrypt_to_hex(encrypted):
    """Convert encrypted numbers to hex"""
    return ",".join(hex(num) for num in encrypted)


def decrypt_from_hex(hex_string):
    """Convert hex back to encrypted numbers"""
    return [int(x, 16) for x in hex_string.split(",")]


# ============================================================================
# EXAMPLE 1: Basic RSA Encryption and Decryption
# ============================================================================
print("=" * 70)
print("EXAMPLE 1: Basic RSA Encryption and Decryption")
print("=" * 70)

print("\n[Step 1] Generating RSA key pair (256-bit for demo)...")
public_key, private_key = generate_keys(bit_length=256)
e, n = public_key
d, _ = private_key

print(f"\nPublic Key:  (e={e}, n={n})")
print(f"Private Key: (d={d}, n={n})")

message = "Hi"
print(f"\n[Step 2] Message to encrypt: '{message}'")

encrypted = encrypt(message, public_key)
print(f"[Step 3] Encrypted: {encrypted}")

decrypted = decrypt(encrypted, private_key)
print(f"[Step 4] Decrypted: '{decrypted}'")
print(f"\nVerification: {'✓ PASS' if decrypted == message else '✗ FAIL'}")


# ============================================================================
# EXAMPLE 2: Public vs Private Key - Who Can Encrypt/Decrypt?
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 2: RSA Asymmetry - Public and Private Keys")
print("=" * 70)

print("""
RSA Security Model:
  
  Bob's Public Key (Available to EVERYONE):
    - Used to ENCRYPT messages to Bob
    - Cannot be used to decrypt
    
  Bob's Private Key (ONLY Bob knows):
    - Used to DECRYPT messages from anyone
    - Must be kept SECRET
    - Cannot be derived from public key (factorization is hard)

Analogy:
  - Public Key = Mailbox (anyone can drop mail)
  - Private Key = Mailbox key (only recipient can open)
""")

print("Demonstration:")
message = "Secret"
print(f"Message: '{message}'")

# Anyone can encrypt with public key
encrypted = encrypt(message, public_key)
print(f"Anyone can encrypt: {encrypted}")

# Only Bob (with private key) can decrypt
decrypted = decrypt(encrypted, private_key)
print(f"Only Bob can decrypt: '{decrypted}'")


# ============================================================================
# EXAMPLE 3: Different Key Sizes
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 3: Key Size Comparison")
print("=" * 70)

print("\nKey Size Implications:\n")

key_sizes = [
    (128, "Tiny (128-bit)", "Broken - factors in seconds"),
    (256, "Small (256-bit)", "Broken - factors in hours"),
    (512, "Medium (512-bit)", "Crackable - factors in weeks/months"),
    (1024, "Standard (1024-bit)", "Becoming weak - not recommended"),
    (2048, "Strong (2048-bit)", "Secure - recommended for today"),
    (4096, "Very Strong (4096-bit)", "Very secure - future-proof"),
]

print("Bit Length | Name                    | Security Status")
print("-" * 60)
for bits, name, status in key_sizes:
    print(f"{bits:4d}      | {name:23s} | {status}")

print("\n✓ Current recommendation: 2048-bit or 4096-bit RSA")
print("✗ Avoid: 512-bit and 1024-bit (being deprecated)")


# ============================================================================
# EXAMPLE 4: Character-by-Character Encryption
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 4: Character-by-Character RSA Operation")
print("=" * 70)

message = "ABC"
print(f"\nMessage: '{message}'")
print(f"Public Key: (e={e}, n={n})\n")

print("Each character encrypted separately:\n")
for i, char in enumerate(message):
    m = ord(char)
    c = pow(m, e, n)
    print(f"  '{char}' (ASCII {m:3d}) -> {c}")

print("\nDecryption (using private key):\n")
encrypted_nums = encrypt(message, public_key)
for i, c in enumerate(encrypted_nums):
    m = pow(c, d, n)
    print(f"  {c} -> (ASCII {m:3d}) '{chr(m)}'")


# ============================================================================
# EXAMPLE 5: Message Length Limitations
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 5: Message Length Limitations")
print("=" * 70)

print(f"""
RSA Limitation:

Each character is encrypted separately.
The encrypted value must be < n (the modulus).

Maximum plaintext value < n
Since ASCII characters are 0-255:
  - This works fine for single characters
  - Each character's ASCII value is definitely < n

For the current key with n={n}:
  Maximum ASCII value per character: 255 (limit)
  Current n value: {n}
  
✓ No problem - n is much larger than 255

Key size determines maximum ASCII value:
  128-bit n:  Can encrypt any ASCII character ✓
  256-bit n:  Can encrypt any ASCII character ✓
  ...
  Standard RSA padding schemes (OAEP) handle this better
""")

# Show it works
test_message = "Hello, World! 123"
print(f"Test message: '{test_message}'")
test_enc = encrypt(test_message, public_key)
test_dec = decrypt(test_enc, private_key)
print(f"Decrypted:    '{test_dec}'")
print(f"Match:        {'✓ YES' if test_dec == test_message else '✗ NO'}")


# ============================================================================
# EXAMPLE 6: Encryption Output Format
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 6: Encryption Output Formats")
print("=" * 70)

message = "Hi"
encrypted = encrypt(message, public_key)

print(f"\nMessage: '{message}'")
print(f"\nEncrypted output formats:")
print(f"\n1. List of numbers:")
print(f"   {encrypted}")

print(f"\n2. Hexadecimal:")
hex_format = encrypt_to_hex(encrypted)
print(f"   {hex_format}")

print(f"\n3. Back to decimal from hex:")
recovered = decrypt_from_hex(hex_format)
print(f"   {recovered}")

print(f"\n4. Decrypted:")
decrypted = decrypt(recovered, private_key)
print(f"   '{decrypted}'")


# ============================================================================
# EXAMPLE 7: Multiple Recipients
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 7: Sending Same Message to Multiple Recipients")
print("=" * 70)

message = "Important"

# Generate keys for 3 recipients
print(f"\nMessage: '{message}'")
print(f"\nGenerating keys for 3 recipients...\n")

recipients = {}
for i in range(1, 4):
    pub_key, priv_key = generate_keys(bit_length=256)
    recipients[f"Person{i}"] = {"public": pub_key, "private": priv_key}
    print(f"Person{i} public key generated")

print(f"\nEncrypting message for each recipient:\n")
for name, keys in recipients.items():
    encrypted = encrypt(message, keys["public"])
    print(f"  {name}: {encrypt_to_hex(encrypted)[:50]}...")

print(f"\nEach recipient can decrypt with their private key:\n")
for name, keys in recipients.items():
    encrypted = encrypt(message, keys["public"])
    decrypted = decrypt(encrypted, keys["private"])
    print(f"  {name}: '{decrypted}'")


# ============================================================================
# EXAMPLE 8: Digital Signatures (Reverse RSA)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 8: Digital Signatures (Conceptual)")
print("=" * 70)

print("""
Digital Signature Process:

1. Alice creates a message
2. Alice "signs" it with her PRIVATE key
3. Anyone can verify with Alice's PUBLIC key
4. Proves: message is from Alice (authentication)
5. Proves: message hasn't been tampered with (integrity)

This is REVERSE RSA usage:
  - Normal:    Encrypt with public key, decrypt with private key
  - Signature: "Encrypt" with private key, verify with public key
""")

message = "I agree"
print(f"\nMessage: '{message}'")

# Simulate signature (using private key to "encrypt")
print(f"\nAlice signs with her private key:")
d, n = recipients["Person1"]["private"]
signature = []
for char in message:
    m = ord(char)
    sig = pow(m, d, n)  # Sign with private key
    signature.append(sig)

print(f"Signature: {encrypt_to_hex(signature)[:50]}...")

# Verify signature (using public key)
print(f"\nAnyone can verify with Alice's public key:")
e, n = recipients["Person1"]["public"]
verified = ""
for sig_value in signature:
    m = pow(sig_value, e, n)  # Verify with public key
    verified += chr(m)

print(f"Verified message: '{verified}'")
print(f"Authentic: {'✓ YES' if verified == message else '✗ NO'}")


# ============================================================================
# EXAMPLE 9: Security - Factorization Problem
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 9: RSA Security - The Factorization Problem")
print("=" * 70)

print("""
RSA Security relies on:

PUBLIC INFORMATION:
  - n (product of p and q)
  - e (public exponent)

PRIVATE INFORMATION (kept secret):
  - d (private exponent)
  - p and q (the prime factors)

ATTACK:
To break RSA, attacker needs to find d.
To find d, attacker needs p and q.
To find p and q, attacker must FACTOR n.

FACTORIZATION IS HARD:
  n = p × q
  
  If n is 2048-bit (617 digits):
    - Time to factor: > 300 trillion years (current tech)
    - Computers needed: More than all atoms in universe
    - This makes RSA practical and secure
    
Example from our demo:
""")

print(f"n = {n}")
print(f"\nFactoring this 256-bit n is computationally hard")
print("(Though practical for brute force given enough time)")
print("\nReal 2048-bit numbers are astronomically harder!")


# ============================================================================
# EXAMPLE 10: Comparison with Other Ciphers
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 10: RSA vs Other Encryption Methods")
print("=" * 70)

print("\n" + "-" * 70)
print("Caesar Cipher")
print("-" * 70)
print("  Key space: 25 possible keys")
print("  Time to crack: < 1 second")
print("  Security: ✗ VERY WEAK")

print("\n" + "-" * 70)
print("XOR Cipher")
print("-" * 70)
print("  Key space: 2^(key_length × 8)")
print("  Time to crack: Depends on key length and patterns")
print("  Security: ✗ WEAK (vulnerable to frequency analysis)")

print("\n" + "-" * 70)
print("RSA (Asymmetric)")
print("-" * 70)
print("  Key space: 2^(key_size) (e.g., 2^2048)")
print("  Time to crack: > 300 trillion years (2048-bit)")
print("  Security: ✓ STRONG (factorization is hard)")
print("  Key advantage: Different keys for encryption/decryption")

print("\n" + "-" * 70)
print("AES (Symmetric, Modern)")
print("-" * 70)
print("  Key space: 2^256")
print("  Time to crack: > 10^77 years (brute force)")
print("  Security: ✓ STRONG (practical for today)")
print("  Advantage: Much faster than RSA")


# ============================================================================
# EXAMPLE 11: Practical Use Cases
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 11: Real-World RSA Applications")
print("=" * 70)

print("""
Where RSA is Used:

1. HTTPS/SSL/TLS
   ✓ Encrypts your browser-to-website connection
   ✓ Example: https://www.google.com
   
2. Email Encryption (PGP/GPG)
   ✓ Securely send emails with encryption
   ✓ Everyone knows Bob's public key
   ✓ Only Bob can decrypt
   
3. Digital Certificates
   ✓ Verify that website is really Google
   ✓ Certificate signed with Google's private key
   ✓ Browser verifies with Google's public key
   
4. Cryptocurrency (Bitcoin, Ethereum)
   ✓ Digital wallets use RSA-like schemes (ECDSA)
   ✓ Your private key = your money
   
5. Code Signing
   ✓ Verify software came from trusted developer
   ✓ Developer signs code with private key
   ✓ Users verify with public key
   
6. Authentication
   ✓ SSH public key authentication
   ✓ SSH certificates
""")

# Example: Simple key exchange concept
print("\n" + "-" * 70)
print("Example: Secure Communication")
print("-" * 70)

alice_pub, alice_priv = generate_keys(bit_length=256)
bob_pub, bob_priv = generate_keys(bit_length=256)

print("\nAlice sends message to Bob:")
msg_to_bob = "Meet tomorrow"
print(f"  Message: '{msg_to_bob}'")

encrypted_for_bob = encrypt(msg_to_bob, bob_pub)
print(f"  Encrypted with Bob's public key: ...")

print(f"\nBob receives and decrypts:")
decrypted_by_bob = decrypt(encrypted_for_bob, bob_priv)
print(f"  Decrypted: '{decrypted_by_bob}'")
print(f"  Match: {'✓ YES' if decrypted_by_bob == msg_to_bob else '✗ NO'}")


# ============================================================================
# EXAMPLE 12: Key Size and Security Time
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 12: Key Size and Security Over Time")
print("=" * 70)

print("""
Recommended Key Sizes by Year:

Year    | Recommended | Acceptable | Avoid
--------|-------------|------------|-----------
2000    | 768-bit     | 512-bit    | 256-bit
2010    | 1024-bit    | 768-bit    | 512-bit
2020    | 2048-bit    | 1024-bit   | 768-bit
2030    | 3072-bit    | 2048-bit   | 1024-bit
2040    | 4096-bit    | 3072-bit   | 2048-bit

Current (2024):
  ✓ SECURE:    2048-bit, 3072-bit, 4096-bit
  ⚠ WEAK:      1024-bit (declining)
  ✗ BROKEN:    512-bit, 768-bit, 1024-bit

Why? Computers get faster, attacks improve.
Moore's Law: Computing power doubles every 2 years.
""")


# ============================================================================
# EXAMPLE 13: Hybrid Encryption (RSA + AES)
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 13: Hybrid Encryption (RSA + Symmetric)")
print("=" * 70)

print("""
Problem with Pure RSA:
  - SLOW: RSA operations are mathematically intensive
  - Message limit: Can only encrypt small amounts
  
Solution: Hybrid Encryption

Process:
  1. Generate random symmetric key (e.g., AES key)
  2. Encrypt large message with fast symmetric cipher (AES)
  3. Encrypt the symmetric key with RSA (public key)
  4. Send: (encrypted_symmetric_key, encrypted_message)
  
Decryption:
  1. Decrypt symmetric key with RSA (private key)
  2. Decrypt message with decrypted symmetric key
  
Benefits:
  ✓ RSA: Solves key distribution problem
  ✓ AES: Encrypts large data quickly
  ✓ Combined: Best of both worlds!

Real-world: HTTPS, PGP, Signal messenger all use this!
""")


# ============================================================================
# EXAMPLE 14: Security Tips
# ============================================================================
print("\n" + "=" * 70)
print("EXAMPLE 14: RSA Security Best Practices")
print("=" * 70)

print("""
DO's:
  ✓ Use 2048-bit or larger keys
  ✓ Keep private key SECRET and secure
  ✓ Use OAEP padding with RSA
  ✓ Combine with symmetric encryption for large data
  ✓ Change keys periodically
  ✓ Verify key authenticity (certificates)
  ✓ Use trusted libraries (not custom implementations)

DON'Ts:
  ✗ Use small keys (< 2048-bit)
  ✗ Share your private key
  ✗ Use bare RSA without padding
  ✗ Encrypt very large messages with RSA alone
  ✗ Reuse keys across systems
  ✗ Trust keys without verification
  ✗ Implement RSA yourself (use proven libraries!)

For this education demo:
  This is simplified RSA (no OAEP padding).
  Real implementations add padding for security.
""")

print("\n" + "=" * 70)
print("END OF RSA EXAMPLES")
print("=" * 70)
