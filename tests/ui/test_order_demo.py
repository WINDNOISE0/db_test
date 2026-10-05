# -----------------------------------------------------
from dataclasses import dataclass, replace

from playwright.sync_api import Page, expect

from ui.pages.login_page import LoginPage
from ui.pages.secure_page import SecurePage


@dataclass(frozen=True)
class User:
    username: str
    password: str


DEFAULT_USER = User(username='tomsmith', password='SuperSecretPassword!')


def test_login_with_wrong_password(page: Page):
    user = replace(DEFAULT_USER, password='wrong_password')

    login_page = LoginPage(page).open()
    login_page.login(user.username, user.password)

    expect(login_page.flash).to_contain_text("Your password is invalid!")


def test_login_with_default_user(page: Page):
    login_page = LoginPage(page).open()
    login_page.login(DEFAULT_USER.username, DEFAULT_USER.password)

    SecurePage(page).should_be_loaded()
