#!/usr/bin/env python3

"""
Simple test to verify basic functionality without any external dependencies.
This test can run in any Python environment.
"""

import unittest

class TestBasicFunctionality(unittest.TestCase):
    """Basic functionality tests that don't require any external dependencies"""
    
    def test_basic_math(self):
        """Test basic mathematical operations"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(10 - 5, 5)
        self.assertEqual(3 * 4, 12)
        self.assertEqual(15 / 3, 5)
    
    def test_string_operations(self):
        """Test basic string operations"""
        test_string = "USB Device Monitor"
        self.assertIn("USB", test_string)
        self.assertEqual(len(test_string), 18)
        self.assertTrue(test_string.startswith("USB"))
    
    def test_list_operations(self):
        """Test basic list operations"""
        devices = ["device1", "device2", "device3"]
        self.assertEqual(len(devices), 3)
        self.assertIn("device1", devices)
        self.assertEqual(devices[0], "device1")
    
    def test_dict_operations(self):
        """Test basic dictionary operations"""
        device_info = {
            "manufacturer": "Test Corp",
            "product": "Test Device",
            "serial": "123456"
        }
        self.assertEqual(device_info["manufacturer"], "Test Corp")
        self.assertIn("product", device_info)
        self.assertEqual(len(device_info), 3)

if __name__ == '__main__':
    unittest.main()
