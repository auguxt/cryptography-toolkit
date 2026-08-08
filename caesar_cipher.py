# Caesar Cipher
# Shifts each letter by a fixed number

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            # Keep uppercase or lowercase
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char  # Keep spaces, numbers, symbols as is
    return result


def decrypt(text, shift):
    return encrypt(text, -shift)  # Just reverse the shift


def brute_force(text):
    print("Trying all 25 possible shifts:")
    for shift in range(1, 26):
        print(f"  Shift {shift}: {decrypt(text, shift)}")


# --- Try it out ---
message = "Hello World"
shift = 3

encrypted = encrypt(message, shift)
decrypted = decrypt(encrypted, shift)

print(f"Original:  {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")

print()
brute_force("Khoor Zruog")
