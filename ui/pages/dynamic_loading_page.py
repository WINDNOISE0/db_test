from playwright.sync_api import Locator

from ui.pages.base_page import BasePage


class DynamicLoadingPage(BasePage):
    path = "/dynamic_loading/2"

    def __init__(self, page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Dynamically Loaded Page Elements")
        self.start_button = page.get_by_role("button", name="Start")
        self.result_text = page.locator("#finish")

    @property
    def unique_element(self) -> Locator:
        return self.heading

    def click_start_loading(self):
        self.start_button.click()

