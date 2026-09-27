import unittest

from scanner import (
    get_service_name,
    validate_ip,
    validate_ports,
    validate_timeout,
    validate_workers,
)


class TestScanner(unittest.TestCase):

    def test_valid_ip(self):
        self.assertTrue(validate_ip("127.0.0.1"))

    def test_invalid_ip(self):
        self.assertFalse(validate_ip("999.999.999.999"))

    def test_valid_ports(self):
        self.assertTrue(validate_ports(20, 100))

    def test_invalid_port_range(self):
        self.assertFalse(validate_ports(100, 20))

    def test_invalid_port_number(self):
        self.assertFalse(validate_ports(0, 100))
        self.assertFalse(validate_ports(20, 70000))

    def test_valid_timeout(self):
        self.assertTrue(validate_timeout(1.0))

    def test_invalid_timeout(self):
        self.assertFalse(validate_timeout(0))
        self.assertFalse(validate_timeout(-1))

    def test_valid_workers(self):
        self.assertTrue(validate_workers(50))

    def test_invalid_workers(self):
        self.assertFalse(validate_workers(0))
        self.assertFalse(validate_workers(-5))

    def test_known_service(self):
        self.assertEqual(get_service_name(22), "SSH")
        self.assertEqual(get_service_name(443), "HTTPS")

    def test_unknown_service(self):
        self.assertEqual(
            get_service_name(9999),
            "Service inconnu"
        )


if __name__ == "__main__":
    unittest.main()
