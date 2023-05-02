"""Main file for running Playtest."""

from datetime import datetime

import pytest

from utils.cli_args import generate_cli_args
from utils.load_config import load_yaml_config

if __name__ == "__main__":
    config = load_yaml_config()
    path_timestamp = f"./reports/{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}"

    cli_args = generate_cli_args(config=config, path=path_timestamp)

    pytest.main(args=cli_args)
