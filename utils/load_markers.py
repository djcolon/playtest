"""Functions for loading pytest markers from the pyproject.toml file."""

import toml


def load_pytest_markers() -> list[str]:
    with open("pyproject.toml", "r") as f:
        toml_data = toml.load(f)
        markers: str = toml_data["tool"]["pytest"]["ini_options"]["markers"]
        m = []
        for x in markers:
            marker_list = x.split(sep=":", maxsplit=1)
            m.append(marker_list[0])
        return m
