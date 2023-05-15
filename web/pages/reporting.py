"""Streamlit page for accessing and viewing reports."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json  # noqa: E402

import streamlit as st  # noqa: E402

from utils.list_paths import list_json_report_files  # noqa: E402


def path_parent(path: Path) -> str:
    """Get the parent folder from a file path."""
    parent = path.parent
    return parent.stem


def load_json_report(file: Path) -> dict:
    """Load a json report."""
    try:
        with open(report_path) as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        err = f"Report file: {file} does not exist."
        print(err)


def get_unique_tests(data: dict) -> tuple[str]:
    """Get all unique node ids from json report."""
    return tuple(set([x["nodeid"] for x in data]))


st.set_page_config(
    page_title="Reports",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Select a json report, formatted to show only parent folder
report_path = st.selectbox(
    label="reports",
    options=list_json_report_files(),
    format_func=path_parent,
)

st.write(f"Selected report: {report_path}")

# Load json report into a dict
data = load_json_report(file=report_path)

# Display the raw json
with st.expander(label="Raw json report data"):
    st.json(data)

# Get total duration from the metadata object
metadata = data.get("metadata")
duration = metadata[1].get("total_duration")

# Display the total test run duration
st.info(body=f"Total duration: {duration}s", icon="⏰")

# Get the test data object from the report
test_data = data.get("test_data")

# Get all unique node ids from the test cases
test_cases = get_unique_tests(test_data)

results = []
for test in test_data:
    if test["when"] == "call":
        test_path = Path(test["nodeid"])
        result_dict = {
            "Test Case": test["nodeid"],
            "Duration": test["duration"],
            "Outcome": test["outcome"],
            "Test Folder": Path(test["location"][0]).parent.stem,
            "Test File": Path(test["location"][0]).name,
        }
        results.append(result_dict)


st.dataframe(results)
