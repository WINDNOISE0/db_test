from playwright.sync_api import Locator

from ui.components.table import Table
from ui.pages.base_page import BasePage


class TablesPage(BasePage):
    path = "/tables"

    def __init__(self, page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Data Tables")
        self.first_table = Table(page.locator("#table1"))
        self.second_table = Table(page.locator("#table2"))

    @property
    def unique_element(self) -> Locator:
        return self.heading

