import os
from .utils import derive_key, compute_hmac, MAGIC, VERSION
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

CHUNK_SIZE = 64 * 1024

HEADER_SIZE = len(MAGIC) + 1 + 16 + 16 + 32  # magic, version, salt, iv, hmac

def decrypt_file(infile, password, overwrite=False):
    with open(infile, 'rb') as fin:
        magic = fin.read(len(MAGIC))
        if magic != MAGIC:
            raise ValueError('Invalid file format (magic bytes mismatch)')
        version = fin.read(1)[0]
        salt = fin.read(16)
        iv = fin.read(16)
        hmac_expected = fin.read(32)
        hint = fin.read(32)
        key = derive_key(password, salt)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        hmac_ctx = compute_hmac(key)
        outfile = infile.replace('.enc', '.dec')
        if os.path.exists(outfile) and not overwrite:
            raise FileExistsError(f'Output file {outfile} exists. Use --overwrite to replace.')
        with open(outfile, 'wb') as fout:
            while True:
                chunk = fin.read(CHUNK_SIZE)
                if not chunk:
                    break
                hmac_ctx.update(chunk)
                decrypted = decryptor.update(chunk)
                fout.write(decrypted)
            decrypted = decryptor.finalize()
            fout.write(decrypted)
        hmac_actual = hmac_ctx.digest()
        if hmac_actual != hmac_expected:
            os.remove(outfile)
            raise ValueError('HMAC verification failed. File may be tampered or password is incorrect.')
    return outfile 