"""File for defining the class for the BMI page."""

from typing import Self

from playwright.sync_api import Locator, Page


class BMIPage:
    """Class to represent the BMI page."""

    URL: str = "https://patient.info/doctor/bmi-calculator-calculator"

    def __init__(self: Self, page: Page) -> None:
        """Initialise the page object and it's defined locators."""
        self.page: Page = page
        self.cookies_agree_btn: Locator = page.get_by_role("button", name="AGREE")
        self.metric_radio_btn: Locator = page.get_by_role("radio", name="Metric")
        self.height_options: Locator = page.get_by_role("combobox")
        self.height_option_cm: Locator = "centimetres"
        self.height_input: Locator = page.get_by_role("textbox", name="Height")
        self.weight_input: Locator = page.get_by_role("textbox", name="Weight")
        self.calculate_btn: Locator = page.get_by_role("button", name="Calculate")
        self.bmi_result: Locator = page.locator(".bmi-result")

    def load(self: Self) -> None:
        """Load the website."""
        self.page.goto(self.URL)
        self.cookies_agree_btn.click()

    def select_metric(self: Self) -> None:
        """Check the metric radio button."""
        self.metric_radio_btn.check()

    def select_metric_cm(self: Self) -> None:
        """Check the metric radio button and select the centimetres option."""
        self.metric_radio_btn.check()
        self.height_options.select_option(self.height_option_cm)

    def input_height_weight(self: Self, height: str, weight: str) -> None:
        """Input the height and weight values."""
        self.height_input.fill(height)
        self.weight_input.fill(weight)

    def calculate_bmi(self: Self) -> None:
        """Click the calculate button."""
        self.calculate_btn.click()
