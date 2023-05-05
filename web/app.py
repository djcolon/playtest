"""Main file for running the Streamlit frontend."""

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components import markers, run, run_config

from utils.cli_args import generate_cli_args
from utils.load_markers import load_pytest_markers

if __name__ == "__main__":
    st.set_page_config(page_title="Playtest", page_icon="random")
    st.title("Playtest")

    with st.sidebar:
        markers = markers()
        run_btn = st.button(label="Run", type="primary")

    if run_btn:
        config = run_config(markers=markers)
        now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        path = Path.cwd() / "reports" / now

        path.mkdir()

        cli_args = generate_cli_args(config=config, path=str(path))

        while True:
            run_playtest = run(cli_args=cli_args)
            if run_playtest is not None:
                break
