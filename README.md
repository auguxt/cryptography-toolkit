# Cryptography Toolkit 🔐

Three simple encryption ciphers built from scratch in Python.
No external libraries needed — just plain Python!

> ⚠️ **For learning only.** Do not use in real projects.

---

## What's Inside

```
cryptography-toolkit/
│
├── caesar_cipher.py
├── xor_cipher.py
├── rsa_cipher.py
│
├── test_caesar.py
├── test_xor.py
├── test_rsa.py
│
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## The 3 Ciphers

### 🔤 Caesar Cipher
Shifts each letter by a fixed number.
```
"HELLO" with shift 3 → "KHOOR"
"KHOOR" with shift 3 → "HELLO"
```

### ⊕ XOR Cipher
XORs each letter with a key. Apply it twice = original back.
```
"Hello" + key "SECRET" → [numbers]
[numbers] + key "SECRET" → "Hello"
```

### 🔑 RSA Cipher
Uses two keys. Encrypt with one, decrypt with the other.
```
Public key  → encrypts the message
Private key → decrypts the message
```

---

## How to Run

```bash
# Run each cipher (shows example output)
python caesar_cipher.py
python xor_cipher.py
python rsa_cipher.py
```

---

## How to Test

```bash
# Run all tests
python -m unittest test_caesar.py test_xor.py test_rsa.py -v

# Or run one at a time
python -m unittest test_caesar.py -v
python -m unittest test_xor.py -v
python -m unittest test_rsa.py -v
```

---

## Requirements

- Python 3.6+
- No external libraries needed

---

## License

MIT — see [LICENSE](LICENSE)
