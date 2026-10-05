import json

from playwright.sync_api import Page, Route

FRUITS_API="*/**/api/v1/fruits"


def mock_fruits(page: Page, fruits: list[dict]) -> None:
    def handle(route: Route) -> None:
        route.fulfill(json=fruits)

    page.route(FRUITS_API, handle)

def add_fruit_to_real_list(page: Page, fruit: dict):
    def handle(route: Route) -> None:
        response = route.fetch()
        fruits_list = response.json()
        fruits_list.append(fruit)
        route.fulfill(response=response, json=fruits_list)

    page.route(FRUITS_API, handle)