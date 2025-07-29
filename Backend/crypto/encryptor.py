import os
from .utils import generate_salt, generate_iv, derive_key, compute_hmac, MAGIC, VERSION
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

CHUNK_SIZE = 64 * 1024

HEADER_SIZE = len(MAGIC) + 1 + 16 + 16 + 32  # magic, version, salt, iv, hmac

def encrypt_file(infile, password, hint=None, overwrite=False):
    if not password:
        raise ValueError('Password must not be empty')
    salt = generate_salt()
    iv = generate_iv()
    key = derive_key(password, salt)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    hmac_ctx = compute_hmac(key)

    outfile = infile + '.enc'
    if os.path.exists(outfile) and not overwrite:
        raise FileExistsError(f'Output file {outfile} exists. Use --overwrite to replace.')

    with open(infile, 'rb') as fin, open(outfile, 'wb') as fout:
        fout.write(MAGIC)
        fout.write(bytes([VERSION]))
        fout.write(salt)
        fout.write(iv)
        fout.write(b'\x00' * 32)  # Placeholder for HMAC
        if hint:
            fout.write(hint.encode('utf-8')[:32].ljust(32, b'\x00'))
        else:
            fout.write(b'\x00' * 32)
        total_data = b''
        while True:
            chunk = fin.read(CHUNK_SIZE)
            if not chunk:
                break
            if len(chunk) % 16 != 0:
                pad_len = 16 - (len(chunk) % 16)
                chunk += bytes([pad_len]) * pad_len
            encrypted = encryptor.update(chunk)
            fout.write(encrypted)
            hmac_ctx.update(encrypted)
            total_data += encrypted
        encrypted = encryptor.finalize()
        fout.write(encrypted)
        hmac_ctx.update(encrypted)
        total_data += encrypted
        hmac_digest = hmac_ctx.digest()
        fout.seek(len(MAGIC) + 1 + 16 + 16)
        fout.write(hmac_digest)
    return outfile 