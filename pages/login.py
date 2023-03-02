from playwright.sync_api import Page


class LoginPage:
    """Class to represent the Login page."""

    URL: str = "https://www.saucedemo.com"
    USERNAME_FIELD: str = "#user-name"
    PASSWORD_FIELD: str = "#password"
    LOGIN_BUTTON: str = "#login-button"

    def __init__(self, page: Page):
        self.page = page

    def load(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.page.locator(self.USERNAME_FIELD).fill(username)
        self.page.locator(self.PASSWORD_FIELD).fill(password)
        self.page.locator(self.LOGIN_BUTTON).click()
