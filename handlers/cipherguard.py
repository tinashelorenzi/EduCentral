from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import base64
import sqlite3
import shutil
import secrets


def derive_key(salt, password):
    """
    Derive a encoded salt key
    This is used by the script entirely
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_pass(pass_str, encrypt_key):
    """Encrypts a password string with encruption key
    pass_str: String password
    encrypt_key: Encryption key
    """
    backend = default_backend()

    salt = b'salt'
    password = encrypt_key.encode()

    key = derive_key(salt, password)
    iv = b'\x01\xec\xfd\x1b\x1e\xc5\xf6['

    if len(iv) != 8:
        raise ValueError("IV size must be 8 bytes")

    cipher = Cipher(algorithms.Blowfish(key),
                    mode=modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(pass_str.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode()


def decrypt_pass(encrypted_pass, encrypt_key):
    """Decrypts an encrypted string using a provided key
    encrypted_pass: Encrypted string
    encrypt_key: Encryption key
    """
    backend = default_backend()

    salt = b'salt'
    password = encrypt_key.encode()

    key = derive_key(salt, password)
    iv = b'\x01\xec\xfd\x1b\x1e\xc5\xf6['

    cipher = Cipher(algorithms.Blowfish(key),
                    mode=modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()

    encrypted_data = base64.b64decode(encrypted_pass)
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(64).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode()



def encrypt_db(input_db_path, output_db_path, encrypt_key):
    """
    Encrypt a database file and rewrite it
    input_db_path: File to encrypt
    output_db_path: File to write the encrypted file to
    encrypt_key: Key to encrypt with
    """
    backend = default_backend()

    salt = b'salt'
    password = encrypt_key.encode()

    key = derive_key(salt, password)
    iv = b'\x01\xec\xfd\x1b\x1e\xc5\xf6['

    cipher = Cipher(algorithms.Blowfish(key), mode=modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    with open(input_db_path, 'rb') as input_file:
        db_data = input_file.read()

    encrypted_data = b''
    for chunk in [db_data[i:i+4096] for i in range(0, len(db_data), 4096)]:
        encrypted_chunk = encryptor.update(chunk) + encryptor.finalize()
        encrypted_data += encrypted_chunk

    with open(output_db_path, 'wb') as output_file:
        output_file.write(encrypted_data)

def decrypt_db(input_db_path, output_db_path, encrypt_key):
    """
    Decrypts file using encryption key
    Decrypt a database file and rewrite it
    input_db_path: File to decrypt
    output_db_path: File to write the decrypted file to
    encrypt_key: Key to decrypt with
    """
    backend = default_backend()

    salt = b'salt'
    password = encrypt_key.encode()

    key = derive_key(salt, password)
    iv = b'\x01\xec\xfd\x1b\x1e\xc5\xf6['
  # Change this to the same value used for encryption
    cipher = Cipher(algorithms.Blowfish(key), mode=modes.CFB(iv), backend=backend)
    decryptor = cipher.decryptor()

    with open(input_db_path, 'rb') as input_file:
        encrypted_data = input_file.read()

    decrypted_data = b''
    for chunk in [encrypted_data[i:i+4096] for i in range(0, len(encrypted_data), 4096)]:
        decrypted_chunk = decryptor.update(chunk) + decryptor.finalize()
        decrypted_data += decrypted_chunk

    with open(output_db_path, 'wb') as output_file:
        output_file.write(decrypted_data)