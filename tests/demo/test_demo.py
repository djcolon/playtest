"""Demo test file for testing the framework."""

import pytest
from playwright.sync_api import expect

from pages.bmi_page import BMIPage


@pytest.mark.parametrize(
    ("height", "weight", "bmi"),
    [("180", "75", "23.15"), ("182", "80", "24.15"), ("184", "85", "25.11")],
)
def test_bmi_metric_centimetres(
    bmi_page: BMIPage, height: str, weight: str, bmi: str
) -> None:
    """Testing the BMI calculator with height (cm) and weight (kg)."""
    # Load the webpage
    bmi_page.load()

    # Input the height and weight
    bmi_page.select_metric_cm()
    bmi_page.input_height_weight(height=height, weight=weight)

    # Click calculate
    bmi_page.calculate_bmi()

    # Assert that the correct BMI is calculated and displayed
    expect(bmi_page.bmi_result).to_have_text(bmi)


@pytest.mark.parametrize(
    ("height", "weight", "bmi"),
    [("1.80", "75", "23.15"), ("1.82", "80", "24.15"), ("1.84", "85", "25.11")],
)
def test_bmi_metric_metres(
    bmi_page: BMIPage, height: str, weight: str, bmi: str
) -> None:
    """Testing the BMI calculator with height (m) and weight (kg)."""
    # Load the webpage
    bmi_page.load()

    # Input the height and weight
    bmi_page.select_metric()
    bmi_page.input_height_weight(height=height, weight=weight)

    # Click calculate
    bmi_page.calculate_bmi()

    # Assert that the correct BMI is calculated and displayed
    expect(bmi_page.bmi_result).to_have_text(bmi)
