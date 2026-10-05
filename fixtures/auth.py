from pathlib import Path
from typing import Callable

import pytest
from filelock import FileLock
from playwright.sync_api import Browser, Page, BrowserContext

from config.settings import settings
from ui.pages.login_page import LoginPage
from ui.pages.secure_page import SecurePage


# @pytest.fixture(scope="session")
# def auth_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory, worker_id: str) -> Path:
#     state_path = tmp_path_factory.mktemp("auth") / "state.json"
#
#     context = browser.new_context(base_url=settings.ui_base_url)
#     try:
#         page = context.new_page()
#         login_page = LoginPage(page).open()
#         login_page.login(settings.ui_username, settings.ui_password.get_secret_value())
#         SecurePage(page).should_be_loaded()
#         context.storage_state(path=state_path)
#     finally:
#         context.close()
#
#     return state_path

def _login_and_save_state(browser: Browser, state_path: Path) -> None:

    context = browser.new_context(base_url=settings.ui_base_url)
    try:
        page = context.new_page()
        login_page = LoginPage(page).open()
        login_page.login(settings.ui_username, settings.ui_password.get_secret_value())
        SecurePage(page).should_be_loaded()
        context.storage_state(path=state_path)
    finally:
        context.close()


@pytest.fixture(scope="session")
def auth_state(browser: Browser, tmp_path_factory: pytest.TempPathFactory, worker_id: str) -> Path:
    if worker_id == "master":
        state_path = tmp_path_factory.mktemp("auth") / "state.json"
        _login_and_save_state(browser, state_path)
        return state_path

    shared_dir = tmp_path_factory.getbasetemp().parent
    state_path = shared_dir / "state.json"
    with FileLock(str(state_path) + ".lock"):
        if not state_path.exists():
            _login_and_save_state(browser, state_path)
    return state_path


@pytest.fixture()
def authorized_page(new_context: Callable[..., BrowserContext], auth_state: Path) -> Page:
    context = new_context(storage_state=auth_state)
    return context.new_page()