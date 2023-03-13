"""Demo test file for testing the framework."""

from playwright.sync_api import expect

from pages.cart import CartPage
from pages.login import LoginPage
from pages.products import ProductsPage


def test_web(
    login_page: LoginPage, products_page: ProductsPage, cart_page: CartPage
) -> None:
    """Test function for testing the framework."""
    # Load the website
    login_page.load()

    # Login to the website
    login_page.login(username="standard_user", password="secret_sauce")

    # Add a product to the cart
    products_page.add_backpack_to_cart()

    # View the cart
    products_page.view_cart()

    # Assert the price is correct
    expect(cart_page.item_price()).to_have_text("$29.99")
