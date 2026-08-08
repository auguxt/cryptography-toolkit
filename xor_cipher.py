# XOR Cipher
# XOR each letter with a key letter

def encrypt(text, key):
    result = []
    for i, char in enumerate(text):
        # XOR the character with the key character (key repeats)
        result.append(ord(char) ^ ord(key[i % len(key)]))
    return result  # Returns a list of numbers


def decrypt(numbers, key):
    result = ""
    for i, num in enumerate(numbers):
        # XOR again with the same key = original character back
        result += chr(num ^ ord(key[i % len(key)]))
    return result


# --- Try it out ---
message = "Hello World"
key = "SECRET"

encrypted = encrypt(message, key)
decrypted = decrypt(encrypted, key)

print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
