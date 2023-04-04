"""Main file for running Playtest."""

import pytest

from utils.cli_args import generate_cli_args
from utils.load_config import load_yaml_config

if __name__ == "__main__":
    config = load_yaml_config()
    cli_args = generate_cli_args(config=config)

    pytest.main(args=cli_args)
