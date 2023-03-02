import pytest
from pages.login import LoginPage
from pages.products import ProductsPage
from pages.cart import CartPage


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def products_page(page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def cart_page(page) -> CartPage:
    return CartPage(page)
