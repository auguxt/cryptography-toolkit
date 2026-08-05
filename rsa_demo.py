"""
Simple RSA Cipher Implementation
Asymmetric encryption using public and private keys
"""

import random
from math import gcd


def gcd_extended(a, b):
    """Extended Euclidean Algorithm to find modular inverse"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


def mod_inverse(e, phi):
    """Find modular inverse of e under modulo phi"""
    gcd_val, x, _ = gcd_extended(e, phi)
    if gcd_val != 1:
        return None
    return (x % phi + phi) % phi


def is_prime(n, k=5):
    """Simple primality test (Miller-Rabin)"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
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
    """Generate a random prime number with given bit length"""
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # Set MSB and LSB
        if is_prime(n):
            return n


def generate_keys(bit_length=512):
    """
    Generate RSA public and private keys
    
    Args:
        bit_length (int): Bit length for prime numbers (default 512 for demo)
    
    Returns:
        tuple: ((e, n), (d, n)) - public key and private key
    """
    # Generate two large prime numbers
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    
    # Calculate n
    n = p * q
    
    # Calculate phi (Euler's totient)
    phi = (p - 1) * (q - 1)
    
    # Choose e (public exponent)
    e = 65537  # Common choice for e
    
    # If e is not coprime with phi, find another
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    
    # Calculate d (private exponent)
    d = mod_inverse(e, phi)
    
    # Public key: (e, n), Private key: (d, n)
    return (e, n), (d, n)


def encrypt(message, public_key):
    """
    Encrypts message using public key
    
    Args:
        message (str): Message to encrypt
        public_key (tuple): Public key (e, n)
    
    Returns:
        list: List of encrypted numbers
    """
    e, n = public_key
    encrypted = []
    
    for char in message:
        # Convert character to number and encrypt
        m = ord(char)
        c = pow(m, e, n)
        encrypted.append(c)
    
    return encrypted


def decrypt(encrypted, private_key):
    """
    Decrypts message using private key
    
    Args:
        encrypted (list): List of encrypted numbers
        private_key (tuple): Private key (d, n)
    
    Returns:
        str: Decrypted message
    """
    d, n = private_key
    decrypted = ""
    
    for c in encrypted:
        # Decrypt each number and convert back to character
        m = pow(c, d, n)
        decrypted += chr(m)
    
    return decrypted


def encrypt_to_hex(encrypted):
    """Convert encrypted numbers to hexadecimal string"""
    return ",".join(hex(num) for num in encrypted)


def decrypt_from_hex(hex_string):
    """Convert hexadecimal string back to encrypted numbers"""
    return [int(x, 16) for x in hex_string.split(",")]


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("RSA CIPHER DEMONSTRATION")
    print("=" * 60)
    
    # Generate RSA keys (using smaller bit length for faster demo)
    print("\n[1] Generating RSA keys (256-bit primes)...")
    public_key, private_key = generate_keys(bit_length=256)
    
    e, n = public_key
    d, _ = private_key
    
    print(f"\nPublic Key (e, n):")
    print(f"  e = {e}")
    print(f"  n = {n}")
    print(f"\nPrivate Key (d, n):")
    print(f"  d = {d}")
    print(f"  n = {n}")
    
    # Encrypt a message
    message = "Hello"
    print(f"\n[2] Encrypting message: '{message}'")
    encrypted = encrypt(message, public_key)
    
    print(f"\nEncrypted numbers: {encrypted}")
    print(f"Encrypted (hex):   {encrypt_to_hex(encrypted)}")
    
    # Decrypt the message
    print(f"\n[3] Decrypting message...")
    decrypted = decrypt(encrypted, private_key)
    
    print(f"Decrypted: '{decrypted}'")
    print(f"\nVerification: {'✓ PASS' if decrypted == message else '✗ FAIL'}")
    
    # Show character-by-character encryption
    print("\n" + "=" * 60)
    print("CHARACTER-BY-CHARACTER ENCRYPTION")
    print("=" * 60)
    print(f"\nOriginal message: {message}")
    print(f"Using public key (e={e}, n={n})\n")
    
    for i, char in enumerate(message):
        m = ord(char)
        c = pow(m, e, n)
        m_dec = pow(c, d, n)
        print(f"  '{char}' (ASCII {m:3d}) -> {c:10d} -> '{chr(m_dec)}' (ASCII {m_dec:3d})")
    
    # Demonstrate security concept
    print("\n" + "=" * 60)
    print("SECURITY CONCEPT")
    print("=" * 60)
    print(f"""
The security of RSA relies on the difficulty of factoring n into p and q.

Given:
  - Public key: (e={e}, n={n})
  - Encrypted message available to everyone
  
To break RSA, attacker would need to:
  1. Find factors p and q such that p × q = n
  2. Calculate d using p, q, and e
  3. Decrypt the message using d

With large primes (2048+ bits), factoring n is computationally infeasible
with current technology, making RSA secure.
    """)
