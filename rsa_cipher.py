# RSA Cipher
# Uses two keys: public key to encrypt, private key to decrypt

import random
from math import gcd


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_prime():
    while True:
        n = random.randint(50, 200)
        if is_prime(n):
            return n


def mod_inverse(e, phi):
    # Find d such that (e * d) % phi == 1
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d


def generate_keys():
    p = generate_prime()
    q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    # Pick e that shares no factors with phi
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key


def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]


def decrypt(encrypted, private_key):
    d, n = private_key
    return "".join(chr(pow(num, d, n)) for num in encrypted)


# --- Try it out ---
public_key, private_key = generate_keys()

message = "Hi"

encrypted = encrypt(message, public_key)
decrypted = decrypt(encrypted, private_key)

print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
