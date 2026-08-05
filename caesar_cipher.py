"""
Simple Caesar Cipher Implementation
Shifts each letter by a fixed number of positions in the alphabet
"""

def encrypt(text, shift):
    """
    Encrypts text using Caesar Cipher
    
    Args:
        text (str): The text to encrypt
        shift (int): Number of positions to shift (1-25)
    
    Returns:
        str: Encrypted text
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            # Determine if uppercase or lowercase
            if char.isupper():
                # Shift uppercase letters
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                # Shift lowercase letters
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            # Keep non-alphabetic characters unchanged
            result += char
    
    return result


def decrypt(text, shift):
    """
    Decrypts text using Caesar Cipher
    
    Args:
        text (str): The encrypted text
        shift (int): Number of positions that were shifted
    
    Returns:
        str: Decrypted text
    """
    # Decryption is just encryption with negative shift
    return encrypt(text, -shift)


def brute_force(text):
    """
    Tries all possible Caesar Cipher shifts (1-25)
    
    Args:
        text (str): The encrypted text
    
    Returns:
        dict: All possible decryptions with their shift values
    """
    results = {}
    
    for shift in range(1, 26):
        results[shift] = decrypt(text, shift)
    
    return results


# Example usage
if __name__ == "__main__":
    # Encrypt a message
    message = "Hello World"
    shift_key = 3
    
    encrypted = encrypt(message, shift_key)
    print(f"Original:  {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Shift key: {shift_key}")
    
    # Decrypt the message
    decrypted = decrypt(encrypted, shift_key)
    print(f"Decrypted: {decrypted}")
    
    print("\n--- Brute Force Attack ---")
    encrypted_text = "Khoor Zruog"
    print(f"Encrypted text: {encrypted_text}")
    print("\nPossible decryptions:")
    
    attempts = brute_force(encrypted_text)
    for shift_val, decryption in attempts.items():
        print(f"Shift {shift_val:2d}: {decryption}")
