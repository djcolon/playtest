"""Main file for running the Streamlit frontend."""

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components import run, run_config, run_type  # noqa: E402

from utils.cli_args import generate_cli_args  # noqa: E402


def btn_callbk() -> None:
    """Change state from streamlit buttons."""
    st.session_state.disabled = not st.session_state.disabled


if __name__ == "__main__":
    st.set_page_config(
        page_title="Playtest",
        page_icon="random",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Playtest")

    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    with st.sidebar:
        with st.expander(label="Config options", expanded=True):
            # Option to select if report is generated
            playtest_report = st.checkbox(
                label="Generate report",
                value=True,
                help="Generate a json report for the test session",
                disabled=st.session_state.disabled,
            )

            # Option to select if a Playwright trace is generated
            tracing = st.checkbox(
                label="Tracing",
                help="Generate a playwright trace for each test. See https://playwright.dev/python/docs/trace-viewer-intro",
                disabled=st.session_state.disabled,
            )

            # Option to select headed view
            headed = st.checkbox(
                label="Headed",
                help="Select to show browser when running tests",
                disabled=st.session_state.disabled,
            )

            # Run tests in parallel
            parallel = st.checkbox(
                label="Parallel",
                help="Select to run tests in parallel",
                disabled=st.session_state.disabled,
            )

        st.divider()

        # Select type of test run and associated options
        run_options = run_type(session_state=st.session_state)

        st.divider()

        run_btn = st.button(
            label="Run",
            on_click=btn_callbk,
            type="primary",
            key="run",
            disabled=st.session_state.disabled,
        )

        if st.button(label="Reset", on_click=btn_callbk, type="secondary"):
            st.session_state.disabled = False

    if run_btn:
        config = run_config(
            parallel=parallel,
            headed=headed,
            playtest_report=playtest_report,
            markers=run_options.get("marks"),
            test_dir=run_options["test_folder"],
            test_file=run_options["test_file"],
            test_case=run_options["test_case"],
            tracing=tracing,
        )

        now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        path = Path.cwd() / "reports" / now

        # Create the report subdirectory only if either option is selected
        if playtest_report or tracing:
            path.mkdir()

        cli_args = generate_cli_args(config=config, path=str(path))

        while True:
            run_playtest = run(cli_args=cli_args)
            if run_playtest is not None:
                break
