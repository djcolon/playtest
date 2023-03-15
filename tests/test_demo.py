"""Demo test file for testing the framework."""

from playwright.sync_api import expect

from pages.bmi_page import BMIPage


def test_bmi_metric(bmi_page: BMIPage) -> None:
    """Test function for testing the metric system calculations of the BMI calculator."""
    # Load the webpage
    bmi_page.load()

    # Input the height and weight
    bmi_page.select_metric_cm()
    bmi_page.input_height_weight(height="180", weight="75")

    # Click calculate
    bmi_page.calculate_bmi()

    # Assert that the correct BMI is calculated and displayed
    expect(bmi_page.bmi_result).to_have_text("23.15")
