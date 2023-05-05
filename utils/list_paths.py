"""Functions for gettings lists of files and directories."""

import re
from pathlib import Path


def list_test_folders() -> list[Path]:
    """Return a list of directories nested in the tests directory."""
    # Define path to test directory for all files including "test" in the name
    path = Path("./tests")

    # Return a list of the files
    return [
        item
        for item in path.iterdir()
        if item.is_dir() and "__pycache__" not in item.name
    ]


def list_test_files(dir: Path) -> list[Path]:
    """Return a list of test files nested in the tests directory."""
    # Define path to test directory for all files including "test" in the name
    files = dir.glob("*test*.py")

    # Return a list of the files
    return [x for x in files if x.is_file()]
