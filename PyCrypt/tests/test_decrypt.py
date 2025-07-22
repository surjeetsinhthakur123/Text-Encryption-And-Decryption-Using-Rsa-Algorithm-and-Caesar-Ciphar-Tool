import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto.encryptor import encrypt_file
from crypto.decryptor import decrypt_file

class TestDecryptor(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_secret.txt'
        self.empty_file = 'empty.txt'
        with open(self.test_file, 'w') as f:
            f.write('This is a test secret.')
        with open(self.empty_file, 'w') as f:
            pass
        self.password = 'testpassword'
        self.enc_file = encrypt_file(self.test_file, self.password, overwrite=True)
        self.enc_empty = encrypt_file(self.empty_file, self.password, overwrite=True)

    def tearDown(self):
        for f in [self.test_file, self.empty_file, self.enc_file, self.enc_empty, self.enc_file.replace('.enc', '.dec'), self.enc_empty.replace('.enc', '.dec')]:
            if os.path.exists(f):
                os.remove(f)

    def test_decrypt_normal_file(self):
        dec_file = decrypt_file(self.enc_file, self.password, overwrite=True)
        with open(dec_file, 'r') as f:
            content = f.read().strip()
        self.assertTrue(content.startswith('This is a test secret.'))

    def test_decrypt_empty_file(self):
        dec_file = decrypt_file(self.enc_empty, self.password, overwrite=True)
        with open(dec_file, 'r') as f:
            content = f.read()
        self.assertEqual(content, '')

    def test_decrypt_wrong_password(self):
        with self.assertRaises(Exception):
            decrypt_file(self.enc_file, 'wrongpassword', overwrite=True)

    def test_decrypt_tampered_file(self):
        # Tamper with the encrypted file
        with open(self.enc_file, 'r+b') as f:
            f.seek(-10, os.SEEK_END)
            f.write(b'corruption')
        with self.assertRaises(Exception):
            decrypt_file(self.enc_file, self.password, overwrite=True)

    def test_decrypt_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            decrypt_file('does_not_exist.enc', self.password, overwrite=True)

    def test_decrypt_no_overwrite(self):
        dec_file = decrypt_file(self.enc_file, self.password, overwrite=True)
        with self.assertRaises(FileExistsError):
            decrypt_file(self.enc_file, self.password, overwrite=False)

if __name__ == '__main__':
    unittest.main() 