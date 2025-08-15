# tests/test_auth.py
import unittest
from auth import hash_password, verify_password

class TestAuth(unittest.TestCase):
    def test_hash_and_verify(self):
        pwd = "Secret123!"
        h = hash_password(pwd)
        self.assertNotEqual(h, pwd)
        self.assertTrue(verify_password(h, pwd))
        self.assertFalse(verify_password(h, "WrongPassword"))

if __name__ == "__main__":
    unittest.main()
