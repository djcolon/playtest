"""File for defining pytest fixtures."""

import pytest
from playwright.sync_api import Page

from pages.bmi_page import BMIPage


@pytest.fixture()
def bmi_page(page: Page) -> BMIPage:
    """Pytest fixture to create instance of the BMIPage class."""
    return BMIPage(page)
