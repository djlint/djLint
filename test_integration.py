#!/usr/bin/env python3
"""Test integration with the actual modified files."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_integration():
    # Test loading the actual settings module
    from djlint.settings import find_djlint_toml, find_project_root
    
    print("Testing integration with actual djlint settings module...")
    
    # Use our test directory
    test_dir = Path(__file__).parent / "tests/test_config/test_dot_djlint_toml"
    
    # Test find_djlint_toml
    result = find_djlint_toml(test_dir)
    print(f"find_djlint_toml result: {result}")
    
    # Verify the result is the .djlint.toml file
    expected = test_dir / ".djlint.toml"
    assert result == expected, f"Expected {expected}, got {result}"
    print("✓ find_djlint_toml correctly finds .djlint.toml")
    
    # Test find_project_root
    subdir = test_dir / "subdir"
    subdir.mkdir(exist_ok=True)
    result2 = find_project_root(subdir)
    print(f"find_project_root result: {result2}")
    
    # Should find the test directory as root due to .djlint.toml
    assert result2 == test_dir, f"Expected {test_dir}, got {result2}"
    print("✓ find_project_root correctly finds project root with .djlint.toml")
    
    print("All integration tests passed!")

if __name__ == "__main__":
    test_integration()