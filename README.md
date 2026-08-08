# Cryptography Toolkit 🔐

Simple encryption examples built from scratch in Python.
Easy enough for a beginner to understand!

## What's Inside

| File | What it does |
|------|-------------|
| `caesar_cipher.py` | Shifts letters by a number |
| `xor_cipher.py` | XORs letters with a key |
| `rsa_cipher.py` | Uses two keys (public + private) |

## How to Run

```bash
python caesar_cipher.py
python xor_cipher.py
python rsa_cipher.py
```

## How to Test

```bash
python -m unittest test_caesar.py -v
python -m unittest test_xor.py -v
python -m unittest test_rsa.py -v
```

## How Each Cipher Works

**Caesar Cipher**
```
A B C D E F ...        (original)
D E F G H I ...        (shifted by 3)

"HELLO" → "KHOOR"
```

**XOR Cipher**
```
H XOR S = some number
XOR again with S = H back

"Hello" + key "SECRET" → numbers → "Hello"
```

**RSA Cipher**
```
Two keys generated: public and private
Encrypt with public key  → scrambled numbers
Decrypt with private key → original message
```

## ⚠️ Note

These are for **learning only**.
Do not use for real security — use proper libraries like `cryptography`.
