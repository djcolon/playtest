"""Streamlit page for viewing test data files."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402


def list_csv_data_files() -> list[Path]:
    """List csv data files in the data directory."""
    # Define path to data directory for all files with .csv extension
    csv_files = (Path.cwd() / "data").glob("*.csv")

    # Return a list of the files
    return [x for x in csv_files if x.is_file()]


def path_stem(path: Path) -> str:
    """Get the stem from a file path."""
    return path.stem


st.title("Test Data")

data_file = st.selectbox(
    label="Test Data Files", options=list_csv_data_files(), format_func=path_stem
)

csv_df = pd.read_csv(filepath_or_buffer=data_file)

st.dataframe(data=csv_df, use_container_width=True)
