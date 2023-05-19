"""Streamlit page for accessing and viewing reports."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json  # noqa: E402

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402
from pandas.io.formats.style import Styler  # noqa: E402

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


def get_total_duration(data: dict) -> float:
    """Get total duration from json report."""
    # Get total duration from the metadata object
    metadata = data.get("metadata")
    duration = metadata[1].get("total_duration")
    return duration


def get_results_count(data: dict) -> int:
    """Get the number of tests passed and failed from the json report."""
    # Identify the test data object
    test_data = data.get("test_data")

    # Initialise counters
    passed_count = 0
    failed_count = 0

    # Get number of passed outcomes and increment counter
    for test in test_data:
        if test["when"] == "call":
            if test["outcome"] == "passed":
                passed_count += 1
            else:
                failed_count += 1

    return passed_count, failed_count


def parse_test_results(data: dict, test_cases: tuple[str]) -> list[dict]:
    """Parse the json report for results to pass into a dataframe."""
    # Identify the test data object
    test_data = data.get("test_data")

    # Initialise empty results list
    results = []

    # Get each object for each unique nodeid
    for test in test_cases:
        test_results = {"Test Case": test}
        test_objects = [x for x in test_data if x["nodeid"] == test]
        for test_object in test_objects:
            if test_object["when"] == "call":
                outcome = test_object["outcome"]
                call_duration = test_object["duration"]
            elif test_object["when"] == "setup":
                setup_duration = test_object["duration"]

            elif test_object["when"] == "teardown":
                teardown_duration = test_object["duration"]

        total_duration = call_duration + setup_duration + teardown_duration
        test_results.update(
            {
                "Outcome": outcome,
                "Setup Duration": setup_duration,
                "Call Duration": call_duration,
                "Teardown Duration": teardown_duration,
                "Total Duration": total_duration,
            }
        )

        results.append(test_results)

    return results


def display_test_failures(data: dict) -> None:
    """Parse and display test failure information from json report."""
    # Identify the test data object
    test_data = data.get("test_data")

    # Get failed test report objects
    for test in test_data:
        if test["when"] == "call" and test["outcome"] != "passed":
            error_message = test["longrepr"]["reprtraceback"]["reprentries"][0]["data"][
                "lines"
            ]
            error_message_str = "\n".join([str(line) for line in error_message])
            with st.expander(label=f":red[{test['nodeid']}]"):
                st.subheader("Path:")
                st.text(test["longrepr"]["reprcrash"]["path"])
                st.subheader("Line Number:")
                st.text(test["longrepr"]["reprcrash"]["lineno"])
                st.subheader("Error Message:")
                st.text(error_message_str)


def highlight_rows(row: pd.DataFrame) -> list[str]:
    """Highlight rows in the test results dataframe."""
    value = row.loc["Outcome"]
    color = "#ff2b2b17" if value != "passed" else ""

    return ["background-color: {}".format(color) for r in row]


def style_report_dataframe(df: Styler) -> Styler:
    """Style and format the report dataframe."""
    # Apply conditional highlighting
    df.apply(highlight_rows, axis=1)

    # Format the floats to 2dp
    df.format(
        formatter={
            "Setup Duration": "{:.2f}",
            "Call Duration": "{:.2f}",
            "Teardown Duration": "{:.2f}",
            "Total Duration": "{:.2f}",
        }
    )

    return df


st.set_page_config(
    page_title="Reports",
    page_icon="random",
    layout="wide",
)

st.title(body="Reports")

with st.sidebar:
    # Select a date to filter selectable test reports
    selected_date = st.date_input(label="Select a date").strftime("%d-%m-%Y")

    # Select a json report, formatted to show only parent folder
    report_path = st.selectbox(
        label="Available reports",
        options=list_json_report_files(date=selected_date),
        format_func=path_parent,
    )

    view_report = st.button(label="View Report", type="primary")

if report_path is not None and view_report:
    # Load json report into a dict
    data = load_json_report(file=report_path)

    # Get the test data object from the report
    test_data = data.get("test_data")

    # Get all unique node ids from the test cases
    test_cases = get_unique_tests(test_data)

    # Get count of passed and failed test results
    passed_count, failed_count = get_results_count(data=data)

    # Tabs for separating test run information
    summary_tab, report_tab, raw_data_tab = st.tabs(["Summary", "Report", "Raw Output"])

    with summary_tab:
        # Display test run summary
        st.subheader(body="Test Run Summary")

        # Display how the tests were run i.e. by folder, file, test case, markers
        metadata = data.get("metadata")
        run_type_arg: str = metadata[0]["args"][1]

        if "/" in run_type_arg and ".py" not in run_type_arg:  # folder: tests/demo
            run_type = f"By test folder - {run_type_arg}"
        elif run_type_arg.endswith(".py"):  # file: tests/demo/test_demo.py
            run_type = f"By test file - {run_type_arg}"
        elif (
            "::" in run_type_arg
        ):  # test: tests/demo/test_demo.py::test_bmi_metric_centimetres
            run_type = f"By test case - {run_type_arg}"
        elif (
            metadata[0]["args"][2] == "-m"
        ):  # multiple marks: "-m" "smoke or regression"
            run_type = f"By markers - {metadata[0]['args'][3]}"
        else:
            run_type = "All Tests"

        st.write(f"- Run Type: {run_type}")
        st.write("- Parallel: Yes")
        st.write("- Tracing: No")
        st.write("- Headed: No")
        st.write(f"- Test Report: {report_path}")

    with report_tab:
        st.subheader(body="Test Run Report")

        info_col1, info_col2, info_col3, info_col4 = st.columns(4)

        # Display the total test run duration
        with info_col1:
            st.info(body=f"Total duration: {get_total_duration(data=data)}s", icon="⏰")

        # Display total number of tests
        with info_col2:
            st.info(body=f"Number of tests: {len(test_cases)}", icon="🧮")

        # Display number of tests passed
        with info_col3:
            st.success(body=f"Passed: {passed_count}", icon="✅")

        # Display number of tests failed
        with info_col4:
            st.error(body=f"Failed: {failed_count}", icon="❌")

        # Create a dataframe of the test results, with styling for failed tests
        results_df = pd.DataFrame(
            data=parse_test_results(data=data, test_cases=test_cases)
        )

        # Display a streamlit dataframe widget with styling applied
        st.dataframe(
            data=results_df.style.pipe(style_report_dataframe),
            use_container_width=True,
        )

        # Display expanders with data for each failed test
        st.subheader(body="Failed tests")

        display_test_failures(data=data)

    with raw_data_tab:
        # Display the raw json
        st.json(data)
