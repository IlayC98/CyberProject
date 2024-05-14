def encrypt_number(number, key=7, modulus=1000000000):
    return (number * key) % modulus

def decrypt_number(encrypted_number, key_inverse=pow(7, -1, 1000000000), modulus=1000000000):
    return (encrypted_number * key_inverse) % modulus

def caesar_cipher_encrypt(text, shift=3):
    encrypted_text = ""
    if isinstance(text, str):
        for char in text:
            if char.isalpha():
                shifted = ord(char) + shift
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                encrypted_text += chr(shifted)
            else:
                encrypted_text += char
    elif isinstance(text, int):
        char = chr(text)
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text = chr(shifted)
        else:
            encrypted_text = char
    return encrypted_text

def caesar_cipher_decrypt(text, shift=3):
    return caesar_cipher_encrypt(text, -shift)
#
# # Example usage:
# input_text = "Hello, World!"
# shift = 3
#
# # Encrypt string
# encrypted_text = caesar_cipher_encrypt(input_text, shift)
# print("Encrypted String:", encrypted_text)
#
# 
# # Encrypt character
# char = ord('a')  # ASCII code for character 'A'
# encrypted_char = caesar_cipher_encrypt(char, shift)
# print("Encrypted Char:", encrypted_char)
#
# # Decrypt string
# decrypted_text = caesar_cipher_decrypt(encrypted_text, shift)
# print("Decrypted String:", decrypted_text)
#
# # Decrypt character
# decrypted_char = caesar_cipher_decrypt(encrypted_char, shift)
# print("Decrypted Char:", decrypted_char)
#
#
# # Example usage:
# number = 8
# key = 7
# modulus = 1000000000  # Modulus should be a large prime number for better security
# encrypted_number = encrypt_number(number, key, modulus)
# print("Encrypted Number:", encrypted_number)
#
# # Decrypt the encrypted number
# # To decrypt, you need the inverse of the key modulo the modulus
# # For simplicity, we're assuming the key is relatively prime to the modulus
# key_inverse = pow(key, -1, modulus)
# decrypted_number = decrypt_number(encrypted_number, key_inverse, modulus)
# print("Decrypted Number:", decrypted_number)
#
#
