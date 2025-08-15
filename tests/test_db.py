# tests/test_db.py
import unittest
import os
import sqlite3
from db import initialize_database, create_user, get_user_by_username

class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure a clean test database
        if os.path.exists("prompt_repo.db"):
            os.remove("prompt_repo.db")
        initialize_database()

    def test_user_insertion_and_retrieval(self):
        username = "testuser"
        password_hash = "dummyhash"
        user_id = create_user(username, password_hash)
        user_row = get_user_by_username(username)
        self.assertIsNotNone(user_row)
        self.assertEqual(user_row['id'], user_id)
        self.assertEqual(user_row['username'], username)

    def test_duplicate_user(self):
        username = "dupuser"
        password_hash = "hash1"
        create_user(username, password_hash)
        with self.assertRaises(sqlite3.IntegrityError):
            create_user(username, "hash2")

if __name__ == "__main__":
    unittest.main()
