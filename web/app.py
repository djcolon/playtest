"""Main file for running the Streamlit frontend."""

import streamlit as st
from components import run

st.set_page_config(page_title="Playtest", page_icon="random")
st.title("Playtest")


with st.sidebar:
    run_btn = st.button(label="Run", type="primary")

if run_btn:
    while True:
        run_playtest = run()
        if run_playtest is not None:
            break
