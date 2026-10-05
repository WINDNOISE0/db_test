from playwright.sync_api import Page, Locator, expect

from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    path = '/login'

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role('button', name='Login')
        self.flash = page.locator('#flash')

    @property
    def unique_element(self) -> Locator:
        return self.login_button

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def invalid_username_is_displayed(self):
        return expect(self.flash).to_be_visible()