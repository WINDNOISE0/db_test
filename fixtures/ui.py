from collections.abc import Callable, Iterator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.settings import settings

ARTIFACTS_DIR = Path("artifacts")



@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report


@pytest.fixture(scope="session")
def playwright() -> Iterator[Playwright]:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Iterator[Browser]:
    browser = playwright.chromium.launch(headless=settings.headless)
    yield browser
    browser.close()


@pytest.fixture()
def new_context(browser: Browser, request: pytest.FixtureRequest) -> Iterator[Callable[..., BrowserContext]]:
    contexts: list[BrowserContext] = []

    def _new_context(action_timeout: int = settings.action_timeout,
                     navigation_timeout: int = settings.navigation_timeout,
                     **kwargs) -> BrowserContext:
        kwargs.setdefault("base_url", settings.ui_base_url)
        context = browser.new_context(**kwargs)

        context.set_default_timeout(action_timeout)
        context.set_default_navigation_timeout(navigation_timeout)

        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        contexts.append(context)
        return context

    yield _new_context

    report = getattr(request.node, "rep_call", None)
    failed = report is not None and report.failed

    for index, context in enumerate(contexts):
        name = f"{request.node.name}_{index}"
        if failed:
            ARTIFACTS_DIR.mkdir(exist_ok=True)

            for page_index, page in enumerate(context.pages):
                screenshot_path = ARTIFACTS_DIR / f"{name}_page{page_index}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                allure.attach.file(
                    screenshot_path,
                    name=f"screenshot_context{index}_page{page_index}",
                    attachment_type=allure.attachment_type.PNG,
                )

            trace_path = ARTIFACTS_DIR / f"{name}.zip"
            context.tracing.stop(path=trace_path)
            allure.attach.file(
                trace_path,
                name=f"trace_context{index}",
                attachment_type=allure.attachment_type.ZIP,
            )
        else:
            context.tracing.stop()  # тест прошёл: остановить и выбросить запись
        context.close()


@pytest.fixture()
def context(new_context: Callable[..., BrowserContext]) -> BrowserContext:
    return new_context()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    return context.new_page()
