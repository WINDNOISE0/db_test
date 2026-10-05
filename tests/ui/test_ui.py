def test_open_login_page(page):
    page.goto("/login")

    assert page.title() == "The Internet"


# def test_contexts_are_isolated(browser, context):
#         # Контекст A, первая вкладка: записываем значение
#         page_a1 = context.new_page()
#         page_a1.goto("/login")
#         page_a1.evaluate("localStorage.setItem('user', 'alice')")
#
#         # Контекст A, вторая вкладка: читаем то же значение
#         page_a2 = context.new_page()
#         page_a2.goto("/login")
#         value_a2 = page_a2.evaluate("localStorage.getItem('user')")
#
#         # Контекст B: новый чистый профиль
#         context_b = browser.new_context()
#         page_b = context_b.new_page()
#         page_b.goto(page_a1.url)
#         value_b = page_b.evaluate("localStorage.getItem('user')")
#         context_b.close()
#
#         assert value_a2 == "alice"
#         assert value_b is None

def test_contexts_are_isolated(new_context):
        # Контекст A, первая вкладка: записываем значение
        context_a = new_context()
        page_a1 = context_a.new_page()
        page_a1.goto("/login")
        page_a1.evaluate("localStorage.setItem('user', 'alice')")

        # Контекст A, вторая вкладка: читаем то же значение
        page_a2 = context_a.new_page()
        page_a2.goto("/login")
        value_a2 = page_a2.evaluate("localStorage.getItem('user')")

        # Контекст B: новый чистый профиль
        context_b = new_context()
        page_b = context_b.new_page()
        page_b.goto("/login")
        value_b = page_b.evaluate("localStorage.getItem('user')")

        assert value_a2 == "alice"
        assert value_b is None







