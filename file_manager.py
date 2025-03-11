import os
from crypto import AESCipher  # Ensure you have AESCipher implemented correctly
from auth import login_user  # Import login function from auth.py

# 🔑 Set Encryption Key (Must be 16, 24, or 32 bytes for AES)
ENCRYPTION_KEY = b"securekey123456"  # Change this to a strong key

# 📌 Create an AES Cipher instance
aes = AESCipher(ENCRYPTION_KEY)

# ✅ Function to check if the user is authenticated
def is_authenticated(username):
    return username is not None and username.strip() != ""

# 🔒 Encrypt File
def encrypt_file(file_path, username):
    """Encrypts a file using AES encryption. Only logged-in users can encrypt."""
    
    if not is_authenticated(username):
        print("[❌] Unauthorized! Please log in to encrypt files.")
        return False

    if not os.path.exists(file_path):
        print("[❌] Error: File not found!")
        return False

    try:
        with open(file_path, "rb") as file:
            plaintext = file.read()

        ciphertext = aes.encrypt(plaintext)  

        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, "wb") as enc_file:
            enc_file.write(ciphertext)

        print(f"[✅] File encrypted successfully: {encrypted_file_path}")
        return True

    except Exception as e:
        print(f"[❌] Encryption failed: {e}")
        return False

# 🔓 Decrypt File
def decrypt_file(encrypted_file_path, username, output_path):
    """Decrypts an AES-encrypted file. Only logged-in users can decrypt."""
    
    if not is_authenticated(username):
        print("[❌] Unauthorized! Please log in to decrypt files.")
        return False

    if not os.path.exists(encrypted_file_path):
        print("[❌] Error: Encrypted file not found!")
        return False

    try:
        with open(encrypted_file_path, "rb") as enc_file:
            ciphertext = enc_file.read()

        plaintext = aes.decrypt(ciphertext)

        with open(output_path, "wb") as output_file:
            output_file.write(plaintext)

        print(f"[✅] File decrypted successfully: {output_path}")
        return True

    except Exception as e:
        print(f"[❌] Decryption failed: {e}")
        return False
