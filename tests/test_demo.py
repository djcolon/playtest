"""Demo test file for testing the framework."""

from playwright.sync_api import Page, expect


def test_web(page: Page) -> None:
    """Test function for testing the framework."""
    page.goto("https://www.saucedemo.com")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.locator("#add-to-cart-sauce-labs-backpack").click()
    page.locator("#shopping_cart_container").click()
    expect(page.locator(".inventory_item_price")).to_have_text("$29.99")
