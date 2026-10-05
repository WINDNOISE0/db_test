from playwright.sync_api import Locator, Page

from config.settings import Settings, settings
from ui.pages.base_page import BasePage


class FruitsPage(BasePage):
    path = settings.route_base_url

    def __init__(self, page:Page):
        super().__init__(page)
        self.heading = page.get_by_role('heading', name='Render a List of Fruits')

    def fruit(self, name: str) -> Locator:
        return self.page.get_by_text(name, exact=True)
