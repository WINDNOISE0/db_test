from faker import Faker
from playwright.sync_api import Page, expect

from ui.mocks.fruits import mock_fruits, add_fruit_to_real_list
from ui.pages.fruits_page import FruitsPage


def test_fruits_list_is_mocked(page: Page):
    mock_fruits(page, [{"name": "Strawberry", "id": 21}])

    fruits_page = FruitsPage(page).navigate()

    expect(fruits_page.fruit("Strawberry")).to_be_visible()


def test_add_fruit_mock(page: Page):
    fruit = {"name": "Strawberryr", "id": 21}

    add_fruit_to_real_list(page, fruit)

    fruits_page = FruitsPage(page).open()

    expect(fruits_page.fruit("Strawberryr")).to_be_visible()
    expect(fruits_page.fruit("Strawberry")).to_be_visible()

def test_add_faker_fruit(page: Page):
    faker = Faker()

    word = faker.word()

    fruit = {"name": word, "id": 22}

    add_fruit_to_real_list(page, fruit)

    fruits_page = FruitsPage(page).open()

    expect(fruits_page.fruit(word)).to_be_visible()
    expect(fruits_page.fruit("Strawberry")).to_be_visible()

