from typing import Self

from playwright.sync_api import Locator, Page, expect


class BasePage:
    path: str = '/'

    def __init__(self, page: Page):
        self.page = page
        self.heading = None

    @property
    def unique_element(self) -> Locator:
        return self.heading

    def open(self) -> Self:
        self.page.goto(self.path)
        self.should_be_loaded()
        return self

    def navigate(self) -> Self:
        self.page.goto(self.path)
        return self

    def should_be_loaded(self):
        if not self.unique_element:
            raise NotImplementedError(f'{type(self).__name__} не указала уникальный элемент')
        expect(self.unique_element).to_be_visible()
        return self
