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
    """List test files nested in the tests directory."""
    # Define path to test directory for all files including "test" in the name
    files = dir.glob("*test*.py")

    # Return a list of the files
    return [x for x in files if x.is_file()]


def list_test_cases(file: Path) -> list[str]:
    """List test functions in a test file."""
    # Initialise an empty list
    all_tests = []
    # Iterate over each line in the file
    with open(file=file, mode="r") as f:
        for line in f:
            # Ignore the line if it is a comment
            if line[0] == "#":
                continue

            # If the line includes a function, append the function name to the list
            elif "def" in line:
                regex_line = re.search(r"([A-Za-z0-9]+(_[A-Za-z0-9]+)+)", line)
                all_tests.append(regex_line.group())

    return all_tests


def list_json_report_files() -> list[Path]:
    """List json report files nested in the reports directory."""
    # Define path to reports directory for all json files

    dir = Path.cwd() / "reports"

    files = dir.glob("*/*.json")

    # Return a list of the files
    return [x for x in files if x.is_file()]
