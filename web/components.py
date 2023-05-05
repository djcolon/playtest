"""Functions and streamlit components for use in the Streamlit frontend."""

import subprocess
from enum import StrEnum

import streamlit as st

from utils.list_paths import list_test_folders
from utils.load_markers import load_pytest_markers


class RunType(StrEnum):
    """Represent different run types for Playtest."""

    All = "All"
    Folder = "By test folder"
    File = "By test file"
    TestCase = "By test case"
    Markers = "By marks"


def run_type() -> dict:
    """Display streamlit component for selecting a run type and set values dependant on option."""
    run_option = st.radio(
        label="Run type",
        options=[r.value for r in RunType],
    )

    marks = []
    test_folder = None
    # test_file = None
    # test = None

    if run_option == RunType.Markers:
        marks = markers()

    if run_option == RunType.Folder:
        test_folder = str(
            st.selectbox(label="Test folder", options=list_test_folders())
        )

    # elif run_option == RunType.File:
    # test_folder = st.selectbox(label="test folders", options=list_test_folders())
    # test_file = st.selectbox(
    # label="test file", options=list_test_files(test_folder)
    # )

    # elif run_option == RunType.TestCase:
    # test_folder = st.selectbox(label="test folders", options=list_test_folders())
    # test_file = st.selectbox(
    # label="test file", options=list_test_files(test_folder)
    # )
    # test = st.selectbox(label="test case", options=list_test_cases(test_file))

    return {
        "marks": marks,
        "test_folder": test_folder,
        # "test_file": test_file,
        # "test": test,
    }


def markers() -> list[str | None]:
    """Load pytest marks, display them in streamlit and return the selected markers."""
    # Parse markers from the pyproject.toml file
    all_marks = load_pytest_markers()
    # Display multi select widget with list of markers
    markers = st.multiselect(
        label="Markers",
        options=all_marks,
        help="Select to run tests with the chosen markers",
    )
    # Return the chosen markers
    return markers


def run_config(
    headed: bool,
    parallel: bool,
    playtest_report: bool,
    markers: list,
    test_dir: str = None,
    tracing: bool = False,
) -> dict:
    """Generate Playtest config to pass to the run command."""
    config = {
        "headed": headed,
        "verbose": True,
        "parallel": parallel,
        "playtest-report": playtest_report,
        "marks": markers,
        "test_dir": test_dir,
        "test_file": None,
        "rerun": 0,
        "tracing": tracing,
    }
    return config


def run(cli_args: list) -> int:
    """Entry point for running pytest from Streamlit."""
    args = ["python", "-m", "pytest"]
    args.extend(cli_args)

    st.write(args)

    # Create expanders to contain different pytest output
    expander_metadata = st.expander("Test Run Metadata")
    expander_results = st.expander("Test Results", expanded=True)
    expander_failures = st.expander("Test Failures")

    with st.spinner("Running tests..."):
        process = subprocess.Popen(args=args, stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline().decode().strip()
            if output == "" and process.poll() is not None:
                st.success("Test Run Complete")
                break

            else:
                if output.startswith(
                    (
                        "==",
                        "platform",
                        "cachedir",
                        "rootdir",
                        "configfile",
                        "plugins",
                        "collecting",
                    )
                ):
                    with expander_metadata:
                        st.write(output)
                elif (
                    output.startswith("tests")
                    and "PASSED" in output
                    or output.startswith("[g")
                    and "PASSED" in output
                ):
                    with expander_results:
                        st.success(output)

                elif output.startswith("tests") and "FAILED" in output:
                    with expander_results:
                        st.error(output)
                else:
                    with expander_failures:
                        st.write(output)
    return_code = process.poll()
    return return_code
