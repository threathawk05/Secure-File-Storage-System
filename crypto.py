from Crypto.Cipher import AES
import os

class AESCipher:
    def __init__(self, key):
        self.key = key.ljust(32, b'\0')[:32]  # Ensure 32-byte key

    def encrypt(self, plaintext):
        if not isinstance(plaintext, bytes):  
            raise TypeError("[❌] Encryption failed: Input must be bytes")  

        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return cipher.nonce + tag + ciphertext  # Return as bytes

    def decrypt(self, encrypted_data):
        nonce = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]

        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext  # Return as bytes
