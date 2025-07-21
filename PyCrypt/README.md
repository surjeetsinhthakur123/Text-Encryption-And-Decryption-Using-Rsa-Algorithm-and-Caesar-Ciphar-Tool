# pycryptsafe

A secure, cross-platform CLI tool for password-based file encryption and decryption using AES-256, PBKDF2, and HMAC integrity checks.

## Features
- AES-256 encryption with password-derived key (PBKDF2)
- Salt & IV generation for strong cryptographic security
- Stream-based encryption for large files
- HMAC-SHA256 integrity check
- Auto-wipe decrypted files after timeout (optional)
- Color-coded CLI (Rich)
- Interactive and direct CLI modes
- Test mode for verifying correctness
- Configurable output naming and overwrite policy
- Optional password hint mechanism

## Usage

### Encrypt a file interactively
```
$ pycryptsafe encrypt --file secret.txt
```

### Decrypt with direct args
```
$ pycryptsafe decrypt --file secret.txt.enc --password "mySecret123"
```

### Encrypt in silent mode and auto-wipe decrypted output in 5 mins
```
$ pycryptsafe encrypt -f confidential.pdf -p "myPass" --auto-wipe 300
```

## Security Notes
- Passwords are never stored or logged
- All keys and decrypted files are zeroed from memory after use
- Secure key derivation (configurable rounds)
- Tamper detection with HMAC

## Project Structure
```
pycryptsafe/
├── cli.py             # Entry point
├── crypto/
│   ├── encryptor.py   # Handles encryption
│   ├── decryptor.py   # Handles decryption
│   └── utils.py       # Helpers (salt, key derivation, IV)
├── tests/
│   ├── test_encrypt.py
│   └── test_decrypt.py
├── README.md
├── requirements.txt
└── setup.py
```

## Why Build This?
- Learn real-world cryptography
- Experience with CLI design & secure file handling
- Useful for secure file storage & transfer
- Foundation for advanced security tools 