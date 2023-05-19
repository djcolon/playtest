"""Functions and streamlit components for use in the Streamlit frontend."""

import subprocess
from enum import Enum

import streamlit as st
from streamlit.runtime.state import SessionStateProxy

from utils.list_paths import list_test_cases, list_test_files, list_test_folders
from utils.load_markers import load_pytest_markers


class RunType(str, Enum):
    """Represent different run types for Playtest."""

    All = "All"
    Folder = "By test folder"
    File = "By test file"
    TestCase = "By test case"
    Markers = "By marks"


def run_type(session_state: SessionStateProxy) -> dict:
    """Display streamlit component for selecting a run type and set relevant values."""
    run_option = st.radio(
        label="Run type",
        options=[r.value for r in RunType],
        disabled=session_state.disabled,
    )

    if run_option == RunType.Markers:
        marks = markers(session_state=session_state)
        options = {
            "marks": marks,
            "test_folder": None,
            "test_file": None,
            "test_case": None,
        }

    elif run_option == RunType.Folder:
        test_folder = st.selectbox(
            label="Test folder",
            options=list_test_folders(),
            disabled=session_state.disabled,
        )

        options = {
            "marks": None,
            "test_folder": str(test_folder),
            "test_file": None,
            "test_case": None,
        }

    elif run_option == RunType.File:
        test_folder = st.selectbox(
            label="test folders",
            options=list_test_folders(),
            disabled=session_state.disabled,
        )
        test_file = st.selectbox(
            label="test file",
            options=list_test_files(test_folder),
            disabled=session_state.disabled,
        )

        options = {
            "marks": None,
            "test_folder": None,
            "test_file": str(test_file),
            "test_case": None,
        }

    elif run_option == RunType.TestCase:
        test_folder = st.selectbox(
            label="test folders",
            options=list_test_folders(),
            disabled=session_state.disabled,
        )
        test_file = st.selectbox(
            label="test file",
            options=list_test_files(test_folder),
            disabled=session_state.disabled,
        )
        test_case = st.selectbox(
            label="test case",
            options=list_test_cases(test_file),
            disabled=session_state.disabled,
        )
        formatted_test_case = f"{str(test_file)}::{str(test_case)}"
        options = {
            "marks": None,
            "test_folder": None,
            "test_file": None,
            "test_case": formatted_test_case,
        }

    else:
        options = {
            "marks": None,
            "test_folder": None,
            "test_file": None,
            "test_case": None,
        }

    return options


def markers(session_state: SessionStateProxy) -> list[str | None]:
    """Load pytest marks, display them in streamlit and return the selected markers."""
    # Parse markers from the pyproject.toml file
    all_marks = load_pytest_markers()
    # Display multi select widget with list of markers
    markers = st.multiselect(
        label="Markers",
        options=all_marks,
        help="Select to run tests with the chosen markers",
        disabled=session_state.disabled,
    )
    # Return the chosen markers
    return markers


def run_config(
    headed: bool,
    parallel: bool,
    playtest_report: bool,
    markers: list,
    test_dir: str = None,
    test_file: str = None,
    test_case: str = None,
    tracing: bool = False,
    rerun: int = 0,
) -> dict:
    """Generate Playtest config to pass to the run command."""
    config = {
        "headed": headed,
        "verbose": True,
        "parallel": parallel,
        "playtest-report": playtest_report,
        "marks": markers,
        "test_dir": test_dir,
        "test_file": test_file,
        "test_case": test_case,
        "rerun": rerun,
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
                        "- generated Playtest report file",
                    )
                ):
                    if any(
                        substring in output
                        for substring in ["FAILURES", "short test summary info"]
                    ):
                        with expander_failures:
                            st.write(output)
                    else:
                        with expander_metadata:
                            st.write(output)

                elif output.startswith(("tests", "[g")) and "PASSED" in output:
                    with expander_results:
                        st.success(output)

                elif output.startswith(("tests", "[g")) and "FAILED" in output:
                    with expander_results:
                        st.error(output)

                elif output.startswith(("tests", "[g")) and "RERUN" in output:
                    with expander_results:
                        st.warning(output)

                else:
                    with expander_failures:
                        st.text(output)

    return_code = process.poll()
    return return_code
