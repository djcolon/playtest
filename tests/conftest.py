"""File for defining pytest fixtures."""

import datetime
import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.bmi_page import BMIPage


@pytest.fixture()
def bmi_page(page: Page) -> BMIPage:
    """Pytest fixture to create instance of the BMIPage class."""
    return BMIPage(page)


def pytest_sessionstart(session: pytest.Session):
    session.results = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        report = {
            "nodeid": result.nodeid,
            "when": result.when,
            "outcome": result.outcome,
            "duration": call.duration,
        }

        if call.excinfo is not None:
            report.update(
                {
                    "errors": {
                        "exception_type": call.excinfo.typename,
                        "exception_message_formatted": call.excinfo.exconly(
                            tryshort=True
                        ),
                        "exception_traceback": str(call.excinfo.traceback.__str__()),
                    }
                }
            )

        item.session.results.append(report)


def pytest_sessionfinish(session: pytest.Session):
    with open(
        Path(f"./reports/{str(datetime.datetime.now()).replace(' ', '-')}.json"), "x"
    ) as f:
        json.dump(session.results, f)
