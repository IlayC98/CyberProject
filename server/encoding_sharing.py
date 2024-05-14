class EncryptionManager:
    def __init__(self, key=7, shift=3, modulus=1000000000):
        self.key = key
        self.shift = shift
        self.modulus = modulus
        self.key_inverse = pow(key, -1, modulus)

    def encrypt_number(self, number):
        return (number * self.key) % self.modulus

    def decrypt_number(self, encrypted_number):
        return (encrypted_number * self.key_inverse) % self.modulus

    def caesar_cipher_encrypt(self, text):
        encrypted_text = ""
        if isinstance(text, str):
            for char in text:
                if char.isalpha():
                    shifted = ord(char) + self.shift
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
                shifted = ord(char) + self.shift
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

    def caesar_cipher_decrypt(self, text):
        decrypted_text = ""
        if isinstance(text, str):
            for char in text:
                if char.isalpha():
                    shifted = ord(char) - self.shift
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
                    decrypted_text += chr(shifted)
                else:
                    decrypted_text += char
        elif isinstance(text, int):
            char = chr(text)
            if char.isalpha():
                shifted = ord(char) - self.shift
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
                decrypted_text = chr(shifted)
            else:
                decrypted_text = char
        return decrypted_text


# Example usage:
encryption_manager = EncryptionManager()

# Encrypt and decrypt string using Caesar cipher
input_text = "up"
encrypted_text = encryption_manager.caesar_cipher_encrypt(input_text)
decrypted_text = encryption_manager.caesar_cipher_decrypt(encrypted_text)

print("Encrypted String:", encrypted_text)
print("Decrypted String:", decrypted_text)

# Encrypt and decrypt character using Caesar cipher
char = ord('a')  # ASCII code for character 'a'
encrypted_char = encryption_manager.caesar_cipher_encrypt(char)
decrypted_char = encryption_manager.caesar_cipher_decrypt(encrypted_char)

print("Encrypted Char:", encrypted_char)
print("Decrypted Char:", decrypted_char)

# Encrypt and decrypt number
number = 950
encrypted_number = encryption_manager.encrypt_number(number)
decrypted_number = encryption_manager.decrypt_number(encrypted_number)

print("Encrypted Number:", encrypted_number)
print("Decrypted Number:", decrypted_number)
