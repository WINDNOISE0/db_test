from playwright.sync_api import Locator, Page

from ui.pages.base_page import BasePage


class SecurePage(BasePage):
    path = "/secure"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Secure Area", exact=True)

    @property
    def unique_element(self) -> Locator:
        return self.heading



