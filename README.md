# Cryptography Toolkit 🔐

A simple, educational cryptography toolkit implementing three classic encryption algorithms: Caesar Cipher, XOR Cipher, and RSA. Perfect for learning cryptographic concepts and understanding how encryption works.

**⚠️ Educational Purpose Only**: These implementations are simplified for learning. Do not use in production systems. For real-world encryption, use battle-tested libraries like `cryptography`, `PyCryptodome`, or language-native solutions.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Algorithms](#algorithms)
  - [Caesar Cipher](#caesar-cipher)
  - [XOR Cipher](#xor-cipher)
  - [RSA Cipher](#rsa-cipher)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Security Considerations](#security-considerations)
- [Learning Resources](#learning-resources)
- [Algorithm Comparison](#algorithm-comparison)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting)
- [Support](#support)
- [Disclaimer](#disclaimer)

## Features

✅ **Three Classic Ciphers**
- Caesar Cipher (substitution)
- XOR Cipher (bitwise)
- RSA Cipher (asymmetric)

✅ **Comprehensive Examples**
- 10 detailed Caesar Cipher examples
- 14 detailed XOR Cipher examples
- 14 detailed RSA Cipher examples

✅ **Unit Tests**
- 43 tests for Caesar Cipher
- 51 tests for XOR Cipher
- 60+ tests for RSA Cipher
- 100% pass rate

✅ **Well-Documented Code**
- Inline comments
- Docstrings
- Type hints
- Usage examples

## Project Structure

```
cryptography-toolkit/
├── caesar_cipher.py          # Caesar Cipher implementation
├── xor_cipher.py             # XOR Cipher implementation
├── rsa_cipher.py             # RSA Cipher implementation
├── examples/
│   ├── caesar_example.py     # 10 Caesar Cipher examples
│   ├── xor_example.py        # 14 XOR Cipher examples
│   └── rsa_example.py        # 14 RSA Cipher examples
├── tests/
│   ├── test_caesar.py        # 43 Caesar Cipher tests
│   ├── test_xor.py           # 51 XOR Cipher tests
│   └── test_rsa.py           # 60+ RSA Cipher tests
└── README.md                 # This file
```

## Installation

### Requirements
- Python 3.6+
- No external dependencies for basic ciphers
- Standard library only

### Setup

1. Clone or download the repository:
```bash
git clone https://github.com/auguxt/cryptography-toolkit.git
cd cryptography-toolkit
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. No additional installation needed - just run!

## Quick Start

### Caesar Cipher

```python
from caesar_cipher import encrypt, decrypt

message = "Hello World"
key = 3

encrypted = encrypt(message, key)
print(f"Encrypted: {encrypted}")  # Output: Khoor Zruog

decrypted = decrypt(encrypted, key)
print(f"Decrypted: {decrypted}")  # Output: Hello World
```

### XOR Cipher

```python
from xor_cipher import encrypt, decrypt, to_hex

message = "Hello World"
key = "SECRET"

encrypted = encrypt(message, key)
print(f"Encrypted (hex): {to_hex(encrypted)}")

decrypted = decrypt(encrypted, key)
print(f"Decrypted: {decrypted}")  # Output: Hello World
```

### RSA Cipher

```python
from rsa_cipher import generate_keys, encrypt, decrypt

# Generate key pair
public_key, private_key = generate_keys(bit_length=512)

message = "Secret Message"

# Encrypt with public key (anyone can do this)
encrypted = encrypt(message, public_key)
print(f"Encrypted: {encrypted}")

# Decrypt with private key (only owner has this)
decrypted = decrypt(encrypted, private_key)
print(f"Decrypted: {decrypted}")  # Output: Secret Message
```

## Algorithms

### Caesar Cipher

**What is it?**
- Substitution cipher that shifts letters by a fixed amount
- Also known as "shift cipher" or "ROT-N"
- One of the oldest encryption methods (used by Julius Caesar)

**How it works:**
```
Plaintext:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Shift 3:    D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
```

**Example:**
- Message: "HELLO"
- Shift: 3
- Encrypted: "KHOOR"
- Decrypted: "HELLO"

**Security:** ❌ **VERY WEAK**
- Only 25 possible keys
- Vulnerable to brute force (cracks in < 1 second)
- Pattern analysis reveals patterns easily
- Use only for educational purposes

**Use Cases:**
- Learning basic cryptography concepts
- ROT13 obfuscation (not encryption)
- Puzzle/game ciphers

**Time Complexity:**
- Encryption: O(n) where n = message length
- Decryption: O(n)

### XOR Cipher

**What is it?**
- Bitwise XOR operation between message and key
- Symmetric encryption (same key encrypts and decrypts)
- Fast and simple but weak if key is reused

**How it works:**
```
Message:  H (ASCII 72) = 01001000
Key:      K (ASCII 75) = 01001011
XOR:                     00000011 = 3
```

**Example:**
```python
message = "Hello"
key = "SECRET"
encrypted = encrypt(message, key)  # Returns bytes
decrypted = decrypt(encrypted, key)  # Returns "Hello"
```

**Key Features:**
- **Symmetric**: A XOR B XOR B = A (same key encrypts and decrypts)
- **Fast**: Simple bitwise operation
- **Key repetition**: Short keys repeat for longer messages

**Security:** ⚠️ **WEAK**
- Vulnerable when key is reused on multiple messages
- Weak against frequency analysis
- One-Time Pad variant is theoretically unbreakable (if key is truly random, same length as message, used only once)

**Real-World Use:**
- Temporary data masking (not encryption)
- Part of more complex systems (not standalone)

**Time Complexity:**
- Encryption: O(n)
- Decryption: O(n)

### RSA Cipher

**What is it?**
- Asymmetric encryption using public and private keys
- Based on difficulty of factoring large numbers
- Used in HTTPS, email encryption, digital signatures
- Computationally intensive but cryptographically secure (with proper key size)

**How it works:**

1. **Key Generation:**
   - Choose two large random prime numbers: p and q
   - Calculate n = p × q
   - Calculate φ(n) = (p-1) × (q-1)
   - Choose public exponent e (usually 65537)
   - Calculate private exponent d such that e × d ≡ 1 (mod φ)
   - Public key: (e, n)
   - Private key: (d, n)

2. **Encryption:**
   - Ciphertext: C = M^e mod n (where M is message)
   - Uses public key (available to everyone)

3. **Decryption:**
   - Plaintext: M = C^d mod n
   - Uses private key (only owner has this)

**Example:**
```python
public_key, private_key = generate_keys(bit_length=2048)

message = "Confidential"

# Anyone can encrypt
encrypted = encrypt(message, public_key)

# Only owner can decrypt
decrypted = decrypt(encrypted, private_key)
```

**Security:** ✅ **STRONG** (with proper key size)
- 2048-bit RSA: ~300 trillion years to break (current technology)
- 4096-bit RSA: Even stronger, future-proof
- Security depends on factorization difficulty

**Key Sizes & Recommendations:**
| Bit Length | Status | Use Case |
|-----------|--------|----------|
| 512-bit | ❌ Broken | Avoid (factors in weeks/months) |
| 1024-bit | ⚠️ Weak | Avoid (declining, not recommended) |
| 2048-bit | ✅ Secure | Standard for 2024 |
| 3072-bit | ✅ Strong | High security |
| 4096-bit | ✅ Very Strong | Future-proof |

**Real-World Applications:**
- HTTPS/TLS (secure websites)
- Email encryption (PGP/GPG)
- Digital certificates
- Cryptocurrency (Bitcoin, Ethereum)
- Code signing
- SSH authentication

**Time Complexity:**
- Key generation: O(log n) tests × O(log³ n) multiplication = Slow
- Encryption: O(log³ n) = Slow
- Decryption: O(log³ n) = Slow

**Limitations:**
- Slow compared to symmetric encryption
- Can only encrypt small messages (< n)
- Requires large key sizes for security (2048+ bits)
- Uses more computational resources

## Usage Examples

### Example 1: Encrypting a Message

```python
from caesar_cipher import encrypt, decrypt

message = "The quick brown fox"
shift = 5

encrypted = encrypt(message, shift)
print(f"Encrypted: {encrypted}")

decrypted = decrypt(encrypted, shift)
print(f"Decrypted: {decrypted}")
```

### Example 2: Brute Force Attack

```python
from caesar_cipher import brute_force

encrypted_message = "Khoor Zruog"
print(f"Trying all shifts for: {encrypted_message}\n")

all_attempts = brute_force(encrypted_message)
for shift, decrypted in all_attempts.items():
    print(f"Shift {shift:2d}: {decrypted}")
    
# Output shows shift 3 gives "Hello World"
```

### Example 3: XOR with Hex Conversion

```python
from xor_cipher import encrypt, decrypt, to_hex, from_hex

message = "Secret"
key = "PASSWORD"

encrypted = encrypt(message, key)
hex_data = to_hex(encrypted)
print(f"Encrypted (hex): {hex_data}")

# Convert back and decrypt
encrypted_again = from_hex(hex_data)
decrypted = decrypt(encrypted_again, key)
print(f"Decrypted: {decrypted}")
```

### Example 4: RSA Digital Signatures

```python
from rsa_cipher import generate_keys, sign, verify

public_key, private_key = generate_keys(bit_length=512)

message = "I agree to the terms"

# Alice signs with her private key
signature = sign(message, private_key)

# Anyone can verify with Alice's public key
verified = verify(signature, public_key)

if verified == message:
    print("✓ Signature is valid - message is from Alice")
else:
    print("✗ Signature is invalid")
```

### Example 5: Encrypting for Multiple Recipients

```python
from rsa_cipher import generate_keys, encrypt, decrypt

message = "Company announcement"

# Generate keys for 3 recipients
alice_pub, alice_priv = generate_keys(bit_length=512)
bob_pub, bob_priv = generate_keys(bit_length=512)
charlie_pub, charlie_priv = generate_keys(bit_length=512)

# Encrypt same message for each recipient
enc_alice = encrypt(message, alice_pub)
enc_bob = encrypt(message, bob_pub)
enc_charlie = encrypt(message, charlie_pub)

# Each recipient decrypts with their own private key
msg_alice = decrypt(enc_alice, alice_priv)
msg_bob = decrypt(enc_bob, bob_priv)
msg_charlie = decrypt(enc_charlie, charlie_priv)

print(f"Alice received: {msg_alice}")
print(f"Bob received: {msg_bob}")
print(f"Charlie received: {msg_charlie}")
```

## Testing

### Run All Tests

```bash
# Caesar Cipher tests (43 tests)
python -m unittest tests.test_caesar -v

# XOR Cipher tests (51 tests)
python -m unittest tests.test_xor -v

# RSA Cipher tests (60+ tests)
python -m unittest tests.test_rsa -v

# Run all tests
python -m unittest discover tests/ -v
```

### Test Coverage

**Caesar Cipher (43 tests)**
- Basic operations (encryption/decryption)
- Different shift values
- Case preservation
- Non-alphabetic character handling
- Edge cases (empty strings, long texts)
- Symmetry properties
- Brute force functionality
- Real-world examples

**XOR Cipher (51 tests)**
- Basic encryption/decryption
- Symmetric properties (A XOR B XOR B = A)
- Key length variations
- Different key values
- Special characters and binary data
- Edge cases
- Hexadecimal conversion
- Real-world scenarios

**RSA Cipher (60+ tests)**
- Key generation and properties
- Basic encryption/decryption
- Asymmetric properties
- Digital signatures
- Multiple recipients
- Primality testing
- Modular arithmetic
- Performance and consistency

## Security Considerations

### ⚠️ Important Warnings

**NEVER USE THESE IN PRODUCTION**

These implementations are educational only. They lack:

1. **Padding schemes**: Real RSA uses OAEP padding to prevent attacks
2. **Error handling**: No validation of inputs/outputs
3. **Timing attack resistance**: Vulnerable to timing analysis
4. **Performance optimization**: Slow for production use
5. **Memory protection**: Doesn't clear sensitive data from memory

### For Production Use

**Use these proven libraries instead:**

```python
# Modern encryption
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa

# PyCryptodome (AES, RSA with padding, etc.)
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

# For cryptocurrency
import hashlib  # SHA-256
from ecdsa import SigningKey, VerifyingKey  # ECDSA
```

### Security Best Practices

1. **Caesar Cipher**
   - ❌ Never use for real encryption
   - ✅ Use for learning/education only

2. **XOR Cipher**
   - ❌ Never use standalone for real data
   - ✅ One-Time Pad is theoretically secure if:
     - Key is truly random
     - Key is same length as message
     - Key is used only once
   - ✅ Use as component of larger systems

3. **RSA Cipher**
   - ✅ Use with proven libraries (cryptography, PyCryptodome)
   - ✅ Always use 2048-bit or larger keys
   - ✅ Always use OAEP padding
   - ✅ Never implement from scratch for production
   - ✅ Combine with symmetric encryption for large data (hybrid encryption)

### Key Management

1. **Keep private keys secret**
   - Store securely
   - Use hardware security modules (HSM) for critical keys
   - Never share or transmit unencrypted

2. **Verify public keys**
   - Use certificates
   - Implement key pinning
   - Validate key fingerprints

3. **Key rotation**
   - Rotate keys periodically
   - Have process for compromised key replacement
   - Archive old keys securely

## Learning Resources

### Books

- **"Cryptography Engineering"** by Ferguson, Schneier, and Kohno
  - Comprehensive overview of cryptographic systems
  - Practical guidance on implementation

- **"Introduction to Modern Cryptography"** by Katz and Lindell
  - Theoretical foundations
  - Rigorous mathematical approach

- **"The Code Breaker"** by Walter Isaacson
  - History of cryptography and computing
  - Story of Jennifer Doudna and CRISPR

### Online Resources

- **Khan Academy**: Cryptography section
- **3Blue1Brown**: "How to send secret messages" video series
- **Brilliant.org**: Interactive cryptography lessons
- **CryptoI - UC Davis**: Free online course

### Interactive Tools

- **CyberChef**: Online encryption/decryption tool
- **Cryptool**: Educational cryptography software
- **FactorDB**: Factorize numbers (see RSA vulnerability)

### Practical Exercises

1. **Caesar Cipher**
   - Write a brute-force cracker
   - Analyze letter frequency
   - Implement for different languages

2. **XOR Cipher**
   - Break repeated-key XOR
   - Implement One-Time Pad
   - Explore key reuse vulnerabilities

3. **RSA**
   - Factor small RSA numbers
   - Explore key size impact on security
   - Implement hybrid encryption

## Algorithm Comparison

| Feature | Caesar | XOR | RSA |
|---------|--------|-----|-----|
| **Type** | Symmetric | Symmetric | Asymmetric |
| **Speed** | ⚡ Very Fast | ⚡ Very Fast | 🐢 Slow |
| **Key Size** | 1 number (1-25) | Variable | 2048+ bits |
| **Security** | ❌ Broken | ⚠️ Weak | ✅ Strong |
| **Possible Keys** | 25 | 2^(key_len×8) | 2^2048 |
| **Time to Break** | <1 sec | Minutes-Hours | 300+ trillion yrs |
| **Use Case** | Education | Education | Production (w/ libs) |

## Contribution Guidelines

Contributions welcome! Areas for improvement:

- [ ] Add AES cipher implementation
- [ ] Add Diffie-Hellman key exchange
- [ ] Add SHA hash functions
- [ ] Implement OAEP padding for RSA
- [ ] Add performance benchmarks
- [ ] Create visualization tools
- [ ] Add more examples
- [ ] Improve documentation

## License

This project is provided as-is for educational purposes, under the MIT License.

## FAQ

**Q: Can I use this in production?**
A: No. Use proven cryptography libraries instead (cryptography, PyCryptodome).

**Q: Why is Caesar cipher so weak?**
A: Only 25 possible keys. A computer can try all of them in milliseconds.

**Q: What's the difference between symmetric and asymmetric encryption?**
A: Symmetric uses one key (fast, simple). Asymmetric uses two keys (slower, solves key distribution problem).

**Q: How does RSA work in HTTPS?**
A: RSA encrypts symmetric keys (AES), then AES encrypts the actual data. This combines both algorithms' benefits.

**Q: Is XOR encryption secure?**
A: Only in One-Time Pad form (random key, same length, used once). Otherwise it's weak.

**Q: How long does it take to break 2048-bit RSA?**
A: With current technology: 300+ trillion years. Future quantum computers might break it.

**Q: Should I implement my own cryptography?**
A: No. Use established libraries. Cryptography is easy to get wrong.

## Troubleshooting

**Import errors**
```bash
# Make sure you're in the correct directory
cd /path/to/cryptography-toolkit
python -c "from caesar_cipher import encrypt"
```

**Test failures**
```bash
# Run tests with verbose output
python -m unittest tests.test_caesar -v

# Run specific test class
python -m unittest tests.test_caesar.TestCaesarBasic -v

# Run specific test method
python -m unittest tests.test_caesar.TestCaesarBasic.test_encrypt_word -v
```

**Performance issues**
- RSA is slow by design. For production, use optimized libraries.
- Large messages will take time to process.
- Consider using smaller bit lengths for testing.

## Support

For questions or issues:
1. Check the [FAQ](#faq) section
2. Review example files (examples/*.py)
3. Read test cases (tests/*.py) for usage patterns
4. Create an issue with detailed description

## Disclaimer

⚠️ **Educational Purpose Only**

This toolkit is provided for educational purposes to help understand cryptographic concepts. 

**Do not rely on this code for security-critical applications.**

The implementations are simplified and lack the hardening, optimization, and proven track record necessary for production use.

For any real-world encryption needs:
1. Use established cryptography libraries
2. Have security experts review your implementation
3. Follow OWASP security guidelines
4. Keep dependencies updated
5. Conduct security audits regularly

---

**Happy Learning! 🔐**

Remember: Understanding how cryptography works is the first step to using it responsibly.
