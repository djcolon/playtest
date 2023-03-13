"""File for defining pytest fixtures."""

import pytest
from playwright.sync_api import Page

from pages.cart import CartPage
from pages.login import LoginPage
from pages.products import ProductsPage


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    """Pytest fixture to create instance of the LoginPage class."""
    return LoginPage(page)


@pytest.fixture()
def products_page(page: Page) -> ProductsPage:
    """Pytest fixture to create instance of the ProductsPage class."""
    return ProductsPage(page)


@pytest.fixture()
def cart_page(page: Page) -> CartPage:
    """Pytest fixture to create instance of the CartPage class."""
    return CartPage(page)
