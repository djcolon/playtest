from playwright.sync_api import Page


class CartPage:
    """Class to represent the Cart page."""

    ITEM_PRICE: str = ".inventory_item_price"

    def __init__(self, page: Page):
        self.page = page

    def item_price(self):
        return self.page.locator(self.ITEM_PRICE)
