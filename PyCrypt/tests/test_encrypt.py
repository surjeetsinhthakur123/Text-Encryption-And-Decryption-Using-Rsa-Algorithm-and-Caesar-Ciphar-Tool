import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto.encryptor import encrypt_file

class TestEncryptor(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_secret.txt'
        self.empty_file = 'empty.txt'
        with open(self.test_file, 'w') as f:
            f.write('This is a test secret.')
        with open(self.empty_file, 'w') as f:
            pass
        self.password = 'testpassword'

    def tearDown(self):
        for f in [self.test_file, self.empty_file, self.test_file + '.enc', self.empty_file + '.enc']:
            if os.path.exists(f):
                os.remove(f)

    def test_encrypt_normal_file(self):
        out_file = encrypt_file(self.test_file, self.password, overwrite=True)
        self.assertTrue(os.path.exists(out_file))
        self.assertGreater(os.path.getsize(out_file), 0)

    def test_encrypt_empty_file(self):
        out_file = encrypt_file(self.empty_file, self.password, overwrite=True)
        self.assertTrue(os.path.exists(out_file))
        self.assertGreater(os.path.getsize(out_file), 0)

    def test_encrypt_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            encrypt_file('does_not_exist.txt', self.password, overwrite=True)

    def test_encrypt_no_overwrite(self):
        out_file = encrypt_file(self.test_file, self.password, overwrite=True)
        with self.assertRaises(FileExistsError):
            encrypt_file(self.test_file, self.password, overwrite=False)

    def test_encrypt_with_empty_password(self):
        with self.assertRaises(Exception):
            encrypt_file(self.test_file, '', overwrite=True)

if __name__ == '__main__':
    unittest.main() 