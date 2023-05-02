"""File for defining pytest fixtures."""


import json
from pathlib import Path

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
        action="store",
        metavar="path",
        default=None,
        help="Path to json report of test session events.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure the playtest-report plugin."""
    playtest_report = config.option.playtest_report
    if playtest_report and not hasattr(config, "workerinput"):
        config._playtest_report_plugin = PlaytestReportPlugin(
            config, Path(playtest_report)
        )
        config.pluginmanager.register(config._playtest_report_plugin)


class PlaytestReportPlugin:
    """Class containing logic for using pytest hooks to create a json report file."""

    def __init__(self, config: pytest.Config, report_path: Path) -> None:
        """Initialise the object with a unique report file path."""
        self._config = config
        self._report_path = report_path / "playtest_report.json"
        self._metadata: list = []
        self._collect_data: list = []
        self._test_data: list = []
        self._total_duration: float = 0

        # Create the report path directory if it does not already exist
        report_path.mkdir(parents=True, exist_ok=True)

    def pytest_collectreport(self, report: pytest.CollectReport) -> None:
        """Get details of the tests that have been collected."""
        data = self._config.hook.pytest_report_to_serializable(
            config=self._config, report=report
        )
        self._collect_data.append(data)

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        """Get details of the tests that have been run."""
        data = self._config.hook.pytest_report_to_serializable(
            config=self._config, report=report
        )

        # Remove the "node" item as it is not json encodable
        if "node" in data:
            data.pop("node")

        self._test_data.append(data)

    def pytest_sessionfinish(self, exitstatus: int) -> None:
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

    def pytest_terminal_summary(self, terminalreporter: TerminalReporter) -> None:
        """Write details of the test report to the terminal."""
        terminalreporter.write_sep(
            "-", f"generated Playtest report file: {self._report_path}"
        )
