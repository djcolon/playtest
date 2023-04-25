import subprocess

import streamlit as st


def run_command():
    process = subprocess.Popen(
        args=["python", "-m", "pytest", "-v", "--headed"], stdout=subprocess.PIPE
    )
    expander_metadata = st.expander("Test Run Metadata")
    expander_results = st.expander("Test Results")
    expander_failures = st.expander("Test Failures")
    while True:
        output = process.stdout.readline().decode()
        if output == "" and process.poll() is not None:
            st.success("Test Run Complete")
            break

        if output:
            if output.strip().startswith(
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
                    st.write(output.strip())
            elif "PASSED" in output:
                with expander_results:
                    st.success(output.strip())
            elif "FAILED" in output:
                with expander_results:
                    st.error(output.strip())
            else:
                with expander_failures:
                    st.write(output.strip())
    rc = process.poll()
    return rc


st.title("Playtest")

if st.button("Run"):
    while True:
        run = run_command()
        if run is not None:
            break
