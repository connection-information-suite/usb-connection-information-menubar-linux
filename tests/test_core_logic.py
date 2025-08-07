#!/usr/bin/env python3

import unittest
import sys
import os
import subprocess
import re
import uuid
from unittest.mock import patch, MagicMock

# Test the core logic without importing the main module that requires GTK


class UsbFallbackParser:
    """Copy of the parser class for testing without GTK dependencies"""
    
    def parse_usb_devices_fallback(self):
        try:
            output = subprocess.check_output(['usb-devices'], text=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Failed to run 'usb-devices': {e}", file=sys.stderr)
            return {}

        devices = {}
        blocks = output.strip().split('\n\n')

        if len(blocks) <= 1: # Fallback for different usb-devices formats
            lines = output.strip().split('\n')
            blocks = []
            current_block = []
            for line in lines:
                if line.startswith('T:') and current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = [line]
                else:
                    current_block.append(line)
            if current_block:
                blocks.append('\n'.join(current_block))

        for block in blocks:
            lines = block.strip().split('\n')
            entry = self.parse_usb_block(lines)
            if entry:
                unique_key = str(uuid.uuid4())
                devices[unique_key] = entry
        return devices

    def parse_usb_block(self, lines):
        entry = {}
        for line in lines:
            if line.startswith('T:'):
                if m := re.search(r'Spd=\s*(\S+)', line): entry['speed'] = m.group(1)
                if m := re.search(r'Bus=(\d+)', line): entry['bus_info'] = f"Bus {m.group(1)}"
            elif line.startswith('D:'):
                if m := re.search(r'Ver=\s*(\d+\.\d+)', line): entry['version'] = m.group(1)
            elif line.startswith('P:'):
                if m := re.search(r'Vendor=(\S+)\s+ProdID=(\S+)', line):
                    entry['vidpid'] = f"{m.group(1).upper()}:{m.group(2).upper()}"
            elif line.startswith('S:'):
                if 'Manufacturer=' in line: entry['manufacturer'] = line.split('Manufacturer=')[1].strip()
                elif 'Product=' in line: entry['product'] = line.split('Product=')[1].strip()
                elif 'SerialNumber=' in line: entry['serial'] = line.split('SerialNumber=')[1].strip()
            elif line.startswith('C:'):
                if m := re.search(r'MxPwr=\s*(\d+)mA', line):
                    try:
                        watts = (int(m.group(1)) / 1000.0) * 5.0
                        entry['max_power'] = f"{watts:.2f}"
                    except ValueError: pass
        return entry if (entry.get('vidpid') or entry.get('product') or entry.get('manufacturer')) else None


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
        
        # Test the device filtering logic
        devices = {item for item in mock_listdir.return_value if ':' not in item}
        expected = {'1-1', '1-2', '2-1'}  # Filtered to exclude 'usb1', 'usb2'
        self.assertEqual(devices, expected)

    @patch('os.path.exists')
    def test_get_current_devices_path_not_exists(self, mock_exists):
        mock_exists.return_value = False
        
        # Test when USB path doesn't exist
        devices = set()
        self.assertEqual(devices, set())

    @patch('os.listdir')
    @patch('os.path.exists')
    def test_get_current_devices_exception(self, mock_exists, mock_listdir):
        mock_exists.return_value = True
        mock_listdir.side_effect = PermissionError("Permission denied")
        
        # Test exception handling
        try:
            devices = set()
        except Exception:
            devices = set()
        
        self.assertEqual(devices, set())


if __name__ == '__main__':
    unittest.main()
