import re

from playwright.sync_api import expect, Page

from config.settings import settings
from ui.pages.dynamic_loading_page import DynamicLoadingPage

from ui.pages.login_page import LoginPage
from ui.pages.secure_page import SecurePage
from ui.pages.tables_page import TablesPage




def test_login(page):
    login_page = LoginPage(page).open()
    login_page.login(settings.ui_username, settings.ui_password.get_secret_value())

    SecurePage(page).should_be_loaded()


def test_login_negative(page):
    login_page = LoginPage(page).open()
    login_page.login('faik', settings.ui_password.get_secret_value())

    login_page.invalid_username_is_displayed()


def test_wait_text(page):
    dynamic_loading_page = DynamicLoadingPage(page).open()

    dynamic_loading_page.click_start_loading()
    expect(dynamic_loading_page.result_text).to_have_text("Hello World!", timeout=10_000)


def test_table_has_four_rows(page):
    tables_page = TablesPage(page).open()

    expect(tables_page.first_table.rows).to_have_count(4)


def test_doe_due_amount(page: Page):
    tables_page = TablesPage(page).open()

    first_name = tables_page.first_table.cell(row_text="Doe", column_name="First Name")
    due = tables_page.first_table.cell(row_text="Doe", column_name="Due")

    expect(first_name).to_have_text("Jason")
    expect(due).to_have_text("$100.00")


def test_conway_due_amount(page: Page):
    tables_page = TablesPage(page).open()

    first_name = tables_page.second_table.cell(row_text="Conway", column_name="First Name")
    due = tables_page.second_table.cell(row_text="Conway", column_name="Due")

    expect(first_name).to_have_text("Tim")
    expect(due).to_have_text("$50.00")


def test_secure_page_opens_without_login_form(authorized_page: Page):
    SecurePage(authorized_page).open()

    expect(authorized_page).to_have_url(re.compile(r".*/secure"))


def test_secure_page_redirects_without_login(page):
    SecurePage(page).navigate()
    login_page = LoginPage(page)

    expect(login_page.flash).to_contain_text("You must login to view the secure area!")


