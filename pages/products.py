from playwright.sync_api import Page


class ProductsPage:
    """Class to represent the Products page."""

    ADD_TO_CART_BACKPACK: str = "#add-to-cart-sauce-labs-backpack"
    VIEW_CART: str = "#shopping_cart_container"

    def __init__(self, page: Page):
        self.page = page

    def add_backpack_to_cart(self):
        self.page.locator(self.ADD_TO_CART_BACKPACK).click()

    def view_cart(self):
        self.page.locator(self.VIEW_CART).click()
