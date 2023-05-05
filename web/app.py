"""Main file for running the Streamlit frontend."""

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components import run, run_config, run_type  # noqa: E402

from utils.cli_args import generate_cli_args  # noqa: E402

if __name__ == "__main__":
    st.set_page_config(
        page_title="Playtest",
        page_icon="random",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("Playtest")

    with st.sidebar:
        # Option to select if report is generated
        playtest_report = st.checkbox(
            label="Generate report",
            value=True,
            help="Generate a json report for the test session",
        )

        # Option to select if a Playwright trace is generated
        tracing = st.checkbox(
            label="Tracing",
            help="Generate a playwright trace for each test. See https://playwright.dev/python/docs/trace-viewer-intro",
        )

        # Option to select headed view
        headed = st.checkbox(
            label="Headed", help="Select to show browser when running tests"
        )

        # Run tests in parallel
        parallel = st.checkbox(label="Parallel", help="Select to run tests in parallel")

        st.divider()

        # Select type of test run and associated options
        run_options = run_type()

        st.divider()

        run_btn = st.button(label="Run", type="primary")

    if run_btn:
        config = run_config(
            parallel=parallel,
            headed=headed,
            playtest_report=playtest_report,
            markers=run_options.get("marks"),
            test_dir=run_options["test_folder"],
            tracing=tracing,
        )
        now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        path = Path.cwd() / "reports" / now

        path.mkdir()

        cli_args = generate_cli_args(config=config, path=str(path))

        while True:
            run_playtest = run(cli_args=cli_args)
            if run_playtest is not None:
                break
