from Crypto.Cipher import AES, DES, ARC4
import os

def pad(data):
    """Padding for AES & DES encryption"""
    return data + b"\0" * (16 - len(data) % 16)

def encrypt_file(filepath, method, key):
    with open(filepath, 'rb') as f:
        data = f.read()

    if method == 'AES':
        key = key.ljust(16, '0').encode()[:16]  # Ensure 16-byte key
        cipher = AES.new(key, AES.MODE_CBC, iv=b'0123456789abcdef')
        encrypted_data = cipher.encrypt(pad(data))
    
    elif method == 'DES':
        key = key.ljust(8, '0').encode()[:8]  # Ensure 8-byte key
        cipher = DES.new(key, DES.MODE_CBC, iv=b'12345678')
        encrypted_data = cipher.encrypt(pad(data))

    elif method == 'RC4':
        key = key.encode()
        cipher = ARC4.new(key)
        encrypted_data = cipher.encrypt(data)

    elif method == 'XOR':
        key = key.encode()
        encrypted_data = bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

    else:
        return None

    encrypted_filepath = os.path.join("encrypted_files", os.path.basename(filepath))
    with open(encrypted_filepath, 'wb') as f:
        f.write(encrypted_data)

    return encrypted_filepath

def decrypt_file(filepath, method, key):
    with open(filepath, 'rb') as f:
        encrypted_data = f.read()

    if method == 'AES':
        key = key.ljust(16, '0').encode()[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv=b'0123456789abcdef')
        data = cipher.decrypt(encrypted_data).rstrip(b"\0")

    elif method == 'DES':
        key = key.ljust(8, '0').encode()[:8]
        cipher = DES.new(key, DES.MODE_CBC, iv=b'12345678')
        data = cipher.decrypt(encrypted_data).rstrip(b"\0")

    elif method == 'RC4':
        key = key.encode()
        cipher = ARC4.new(key)
        data = cipher.decrypt(encrypted_data)

    elif method == 'XOR':
        key = key.encode()
        data = bytes([b ^ key[i % len(key)] for i, b in enumerate(encrypted_data)])

    else:
        return None

    decrypted_filepath = os.path.join("decrypted_files", os.path.basename(filepath))
    with open(decrypted_filepath, 'wb') as f:
        f.write(data)

    return decrypted_filepath
