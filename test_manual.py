#!/usr/bin/env python3
"""Simple manual test for .djlint.toml support."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from djlint.settings import find_djlint_toml, find_project_root
    
    # Test 1: Test find_djlint_toml with .djlint.toml only
    test_dir = Path("/tmp/djlint_test_1")
    test_dir.mkdir(exist_ok=True)
    
    dot_djlint_file = test_dir / ".djlint.toml"
    dot_djlint_file.write_text("indent = 2")
    
    result = find_djlint_toml(test_dir)
    print(f"Test 1 - .djlint.toml only: {result}")
    assert result == dot_djlint_file, f"Expected {dot_djlint_file}, got {result}"
    
    # Test 2: Test find_djlint_toml with both files (djlint.toml should take precedence)
    test_dir2 = Path("/tmp/djlint_test_2")
    test_dir2.mkdir(exist_ok=True)
    
    djlint_file = test_dir2 / "djlint.toml"
    djlint_file.write_text("indent = 4")
    
    dot_djlint_file2 = test_dir2 / ".djlint.toml"
    dot_djlint_file2.write_text("indent = 2")
    
    result2 = find_djlint_toml(test_dir2)
    print(f"Test 2 - both files present: {result2}")
    assert result2 == djlint_file, f"Expected {djlint_file}, got {result2}"
    
    # Test 3: Test find_project_root with .djlint.toml
    test_dir3 = Path("/tmp/djlint_test_3")
    test_dir3.mkdir(exist_ok=True)
    
    subdir = test_dir3 / "subdir"
    subdir.mkdir(exist_ok=True)
    
    dot_djlint_file3 = test_dir3 / ".djlint.toml"
    dot_djlint_file3.write_text("indent = 2")
    
    result3 = find_project_root(subdir)
    print(f"Test 3 - project root with .djlint.toml: {result3}")
    assert result3 == test_dir3, f"Expected {test_dir3}, got {result3}"
    
    print("All tests passed!")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Could not import djlint modules. This is expected if dependencies are not installed.")
except Exception as e:
    print(f"Test failed with error: {e}")
    sys.exit(1)