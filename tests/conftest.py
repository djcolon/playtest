"""File for defining pytest fixtures."""


import json
from datetime import datetime
from pathlib import Path
from typing import Self

import pytest
from _pytest.terminal import TerminalReporter
from playwright.sync_api import Page

from pages.bmi_page import BMIPage


# Page fixtures
@pytest.fixture()
def bmi_page(page: Page) -> BMIPage:
    """Pytest fixture to create instance of the BMIPage class."""
    return BMIPage(page)


# Hooks
def pytest_addoption(parser: pytest.Parser) -> None:
    """Add a command line option."""
    parser.addoption(
        "--playtest-report",
        action="store_true",
        default=None,
        help="Generate a json test report.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure the playtest-report plugin."""
    playtest_report = config.option.playtest_report
    if playtest_report and not hasattr(config, "workerinput"):
        config._playtest_report_plugin = PlaytestReportPlugin(config)
        config.pluginmanager.register(config._playtest_report_plugin)


class PlaytestReportPlugin:
    """Class containing logic for using pytest hooks to create a json report file."""

    def __init__(self: Self, config: pytest.Config) -> None:
        """Initialise the object with a unique report file path."""
        self._config = config
        self._report_path = Path(
            f"./reports/{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json"
        )
        self._metadata: list = []
        self._collect_data: list = []
        self._test_data: list = []
        self._total_duration: float = 0

    def pytest_collectreport(self: Self, report: pytest.CollectReport) -> None:
        """Get details of the tests that have been collected."""
        data = self._config.hook.pytest_report_to_serializable(
            config=self._config, report=report
        )
        self._collect_data.append(data)

    def pytest_runtest_logreport(self: Self, report: pytest.TestReport) -> None:
        """Get details of the tests that have been run."""
        data = self._config.hook.pytest_report_to_serializable(
            config=self._config, report=report
        )

        # Remove the "node" item as it is not json encodable
        if "node" in data:
            data.pop("node")

        self._test_data.append(data)

    def pytest_sessionfinish(self: Self, exitstatus: int) -> None:
        """Generate report at the end of the pytest session."""
        # Get the metadata for the report
        data = {"pytest_version": pytest.__version__, "exitstatus": exitstatus}
        self._metadata.append(data)

        # Calculate total duration of test execution
        for x in self._test_data:
            self._total_duration += x["duration"]
        self._metadata.append({"total_duration": round(self._total_duration, 2)})

        # Create a dict from all the lists of data
        json_data = {
            "metadata": self._metadata,
            "collect_data": self._collect_data,
            "test_data": self._test_data,
        }

        # Dump the dictionary as json to the json file
        with open(self._report_path, "x") as f:
            json.dump(json_data, f)

    def pytest_terminal_summary(self: Self, terminalreporter: TerminalReporter) -> None:
        """Write details of the test report to the terminal."""
        terminalreporter.write_sep(
            "-", f"generated Playtest report file: {self._report_path}"
        )
