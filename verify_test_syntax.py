#!/usr/bin/env python3

"""
Simple script to verify the test file syntax is correct.
This doesn't run the tests, just checks that the Python syntax is valid.
"""

import ast
import sys

def verify_syntax(file_path):
    """Verify that a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Try to parse the file
        ast.parse(source)
        print(f"✅ {file_path} - Syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path} - Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path} - Error: {e}")
        return False

def main():
    """Verify all test files"""
    test_files = [
        'tests/test_core_logic.py',
        'test_runner.py'
    ]
    
    print("Verifying test file syntax...")
    print("=" * 40)
    
    all_valid = True
    for file_path in test_files:
        if not verify_syntax(file_path):
            all_valid = False
    
    print("=" * 40)
    if all_valid:
        print("✅ All test files have valid syntax!")
        return 0
    else:
        print("❌ Some test files have syntax errors!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
