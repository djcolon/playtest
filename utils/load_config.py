"""Functions for loading config files."""

import yaml


def load_yaml_config() -> dict:
    """Load the config.yaml file."""
    with open("config.yaml", "r") as f:
        config: dict = yaml.load(stream=f, Loader=yaml.FullLoader)
    return config
