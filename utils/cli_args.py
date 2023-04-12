"""Functions to produce the cli arguments for pytest."""


def generate_cli_args(config: dict) -> list:
    """Return a list of string arguments for the pytest.main() call."""
    cli_args = []

    if config["verbose"]:
        cli_args.append("-v")

    if config["marks"] is not None:
        cli_args.append("-m")
        cli_args.append(" or ".join([str(m) for m in config["marks"]]))

    if config["playtest-report"]:
        cli_args.append("--playtest-report")

    if config["parallel"]:
        cli_args.append("--numprocesses")
        cli_args.append("auto")

    return cli_args
