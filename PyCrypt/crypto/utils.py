import os
import hashlib
import hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

MAGIC = b'PCRYPT'
VERSION = 1

backend = default_backend()


def generate_salt():
    return os.urandom(16)

def generate_iv():
    return os.urandom(16)

def derive_key(password, salt, iterations=200_000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    return kdf.derive(password.encode('utf-8'))

def compute_hmac(key):
    return hmac.new(key, digestmod=hashlib.sha256)

def wipe_file(path):
    if not os.path.exists(path):
        return
    with open(path, 'ba+', buffering=0) as f:
        length = f.tell()
        f.seek(0)
        f.write(os.urandom(length))
    os.remove(path) 