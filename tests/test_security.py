import unittest

from utils.security import hash_password, verify_password


class SecurityTests(unittest.TestCase):
    def test_long_password_is_supported(self):
        long_password = "a" * 80

        hashed = hash_password(long_password)

        self.assertTrue(verify_password(long_password, hashed))


if __name__ == "__main__":
    unittest.main()
