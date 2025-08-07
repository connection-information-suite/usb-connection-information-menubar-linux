#!/usr/bin/env python3

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from usb_device_monitor.main import UsbFallbackParser, UsbMonitor


class TestUsbFallbackParser(unittest.TestCase):
    def setUp(self):
        self.parser = UsbFallbackParser()

    @patch('subprocess.check_output')
    def test_parse_usb_devices_fallback_success(self, mock_check_output):
        # Mock successful usb-devices output
        mock_output = """
T:  Bus=01 Lev=01 Prnt=01 Port=00 Cnt=01 Dev#=  2 Spd=480  MxCh= 0
D:  Ver= 2.00 Cls=00(>ifc ) Sub=00 Prot=00 MxPS=64 #Cfgs=  1
P:  Vendor=0951 ProdID=1666 Rev= 1.00
S:  Manufacturer=Kingston
S:  Product=DataTraveler 3.0
S:  SerialNumber=001CC0EC34E8BB30F9A00B8C
C:* #Ifs= 1 Cfg#= 1 Atr=80 MxPwr=224mA
"""
        mock_check_output.return_value = mock_output
        
        result = self.parser.parse_usb_devices_fallback()
        
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        
        # Check that we have at least one device
        device_info = list(result.values())[0]
        self.assertEqual(device_info.get('manufacturer'), 'Kingston')
        self.assertEqual(device_info.get('product'), 'DataTraveler 3.0')
        self.assertEqual(device_info.get('speed'), '480')

    @patch('subprocess.check_output')
    def test_parse_usb_devices_fallback_command_not_found(self, mock_check_output):
        # Mock FileNotFoundError
        mock_check_output.side_effect = FileNotFoundError("usb-devices: command not found")
        
        result = self.parser.parse_usb_devices_fallback()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)

    def test_parse_usb_block_valid(self):
        lines = [
            "T:  Bus=01 Lev=01 Prnt=01 Port=00 Cnt=01 Dev#=  2 Spd=480  MxCh= 0",
            "D:  Ver= 2.00 Cls=00(>ifc ) Sub=00 Prot=00 MxPS=64 #Cfgs=  1",
            "P:  Vendor=0951 ProdID=1666 Rev= 1.00",
            "S:  Manufacturer=Kingston",
            "S:  Product=DataTraveler 3.0",
            "S:  SerialNumber=001CC0EC34E8BB30F9A00B8C",
            "C:* #Ifs= 1 Cfg#= 1 Atr=80 MxPwr=224mA"
        ]
        
        result = self.parser.parse_usb_block(lines)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.get('manufacturer'), 'Kingston')
        self.assertEqual(result.get('product'), 'DataTraveler 3.0')
        self.assertEqual(result.get('serial'), '001CC0EC34E8BB30F9A00B8C')
        self.assertEqual(result.get('vidpid'), '0951:1666')
        self.assertEqual(result.get('version'), '2.00')
        self.assertEqual(result.get('speed'), '480')
        self.assertEqual(result.get('max_power'), '1.12')

    def test_parse_usb_block_invalid(self):
        lines = [
            "T:  Bus=01 Lev=01 Prnt=01 Port=00 Cnt=01 Dev#=  2 Spd=480  MxCh= 0",
            "D:  Ver= 2.00 Cls=00(>ifc ) Sub=00 Prot=00 MxPS=64 #Cfgs=  1"
            # Missing required fields like Vendor/Product
        ]
        
        result = self.parser.parse_usb_block(lines)
        
        self.assertIsNone(result)


class TestUsbMonitor(unittest.TestCase):
    def setUp(self):
        self.callback_called = False
        self.callback_count = 0
        
    def callback(self):
        self.callback_called = True
        self.callback_count += 1

    @patch('os.listdir')
    @patch('os.path.exists')
    def test_get_current_devices_success(self, mock_exists, mock_listdir):
        mock_exists.return_value = True
        mock_listdir.return_value = ['1-1', '1-2', '2-1', 'usb1', 'usb2']
        
        monitor = UsbMonitor(self.callback)
        result = monitor.get_current_devices()
        
        expected = {'1-1', '1-2', '2-1'}  # Filtered to exclude 'usb1', 'usb2'
        self.assertEqual(result, expected)

    @patch('os.path.exists')
    def test_get_current_devices_path_not_exists(self, mock_exists):
        mock_exists.return_value = False
        
        monitor = UsbMonitor(self.callback)
        result = monitor.get_current_devices()
        
        self.assertEqual(result, set())

    @patch('os.listdir')
    @patch('os.path.exists')
    def test_get_current_devices_exception(self, mock_exists, mock_listdir):
        mock_exists.return_value = True
        mock_listdir.side_effect = PermissionError("Permission denied")
        
        monitor = UsbMonitor(self.callback)
        result = monitor.get_current_devices()
        
        self.assertEqual(result, set())


if __name__ == '__main__':
    unittest.main()
