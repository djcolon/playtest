"""Functions and streamlit components for use in the Streamlit frontend."""

import subprocess

import streamlit as st


def run_config() -> dict:
    """Generate Playtest config to pass to the run command."""
    config = {
        "verbose": True,
        "parallel": False,
        "playtest-report": True,
        "marks": None,
        "test_dir": None,
        "test_file": None,
        "rerun": 0,
        "tracing": False,
    }
    return config


def run(cli_args: list) -> int:
    """Entry point for running pytest from Streamlit."""
    args = ["python", "-m", "pytest", "tests"]
    args.extend(cli_args)

    st.write(args)

    # Create expanders to contain different pytest output
    expander_metadata = st.expander("Test Run Metadata")
    expander_results = st.expander("Test Results")
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
                elif output.startswith("tests") and "PASSED" in output:
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
