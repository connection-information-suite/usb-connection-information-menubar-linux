#!/usr/bin/env python3

"""
Simple test runner for the USB Device Monitor core logic tests.
This script runs the tests without requiring pytest or GTK dependencies.
"""

import sys
import os

# Add the tests directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

# Import and run the tests
from test_core_logic import TestUsbFallbackParser, TestUsbMonitor

def run_tests():
    """Run all tests and report results"""
    import unittest
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestUsbFallbackParser))
    suite.addTests(loader.loadTestsFromTestCase(TestUsbMonitor))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("Running USB Device Monitor Core Logic Tests...")
    print("=" * 50)
    
    exit_code = run_tests()
    
    print("=" * 50)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    sys.exit(exit_code)
