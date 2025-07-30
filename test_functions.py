#!/usr/bin/env python3
"""Simple manual test focusing only on the changed functions."""

import sys
from pathlib import Path

# Test the modified functions directly
def find_djlint_toml(root: Path) -> Path | None:
    """Search upstream for a djlint.toml or .djlint.toml file."""
    djlint_toml = root / "djlint.toml"

    if djlint_toml.is_file():
        return djlint_toml

    # Fall back to .djlint.toml if djlint.toml doesn't exist
    dotted_djlint_toml = root / ".djlint.toml"

    if dotted_djlint_toml.is_file():
        return dotted_djlint_toml

    return None

def find_project_root(src: Path) -> Path:
    """Attempt to get the project root."""
    for directory in (src, *src.parents):
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

        if (directory / "djlint.toml").is_file():
            return directory

        if (directory / ".djlint.toml").is_file():
            return directory

        if (directory / ".djlintrc").is_file():
            return directory

    return directory

# Test the functions
def test():
    import tempfile
    import shutil
    
    # Test 1: Test find_djlint_toml with .djlint.toml only
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        dot_djlint_file = test_dir / ".djlint.toml"
        dot_djlint_file.write_text("indent = 2")
        
        result = find_djlint_toml(test_dir)
        print(f"Test 1 - .djlint.toml only: {result}")
        assert result == dot_djlint_file, f"Expected {dot_djlint_file}, got {result}"
        print("✓ Test 1 passed")
    
    # Test 2: Test find_djlint_toml with both files (djlint.toml should take precedence)
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        djlint_file = test_dir / "djlint.toml"
        djlint_file.write_text("indent = 4")
        
        dot_djlint_file = test_dir / ".djlint.toml"
        dot_djlint_file.write_text("indent = 2")
        
        result = find_djlint_toml(test_dir)
        print(f"Test 2 - both files present: {result}")
        assert result == djlint_file, f"Expected {djlint_file}, got {result}"
        print("✓ Test 2 passed")
    
    # Test 3: Test find_project_root with .djlint.toml
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        subdir = test_dir / "subdir"
        subdir.mkdir(exist_ok=True)
        
        dot_djlint_file = test_dir / ".djlint.toml"
        dot_djlint_file.write_text("indent = 2")
        
        result = find_project_root(subdir)
        print(f"Test 3 - project root with .djlint.toml: {result}")
        assert result == test_dir, f"Expected {test_dir}, got {result}"
        print("✓ Test 3 passed")
        
    # Test 4: Test find_djlint_toml with no files
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        result = find_djlint_toml(test_dir)
        print(f"Test 4 - no config files: {result}")
        assert result is None, f"Expected None, got {result}"
        print("✓ Test 4 passed")
    
    print("All tests passed!")

if __name__ == "__main__":
    test()