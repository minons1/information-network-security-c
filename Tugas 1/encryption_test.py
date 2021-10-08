import pyaes
import pbkdf2
import binascii
import os
import secrets

# Derive a 256-bit AES encryption key from the password
password = "n3wPa55"
passwordSalt = os.urandom(16)
key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
print('AES encryption key:', binascii.hexlify(key))

# Encrypt the plaintext with the given key:
#   ciphertext = AES-256-CTR-Encrypt(plaintext, key, iv)
iv = secrets.randbits(256)
plaintext = "Text for encryption"
aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
ciphertext = aes.encrypt(plaintext)
print('binascii-Encrypted:', binascii.hexlify(ciphertext))
print('ciphertext-Encrypted', ciphertext)
print('type-Encrypted: ', type(ciphertext))

# Decrypt the ciphertext with the given key:
#   plaintext = AES-256-CTR-Decrypt(ciphertext, key, iv)
aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
decrypted = aes.decrypt(ciphertext)
print('Decrypted:', decrypted)

# with open("./aa.jpg", 'rb') as file:
#     readfile = True
#     while (readfile):
#         readfile = file.read(1024)
#         aes.encrypt(readfile)
#         print(binascii.hexlify(readfile))
#         print("\n")