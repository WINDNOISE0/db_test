from playwright.sync_api import Locator

class Table:
    def __init__(self, root:Locator) -> None:
        self.root = root
        self.headers = root.locator("thead th")
        self.rows = root.locator("tbody tr")

    def column_index(self, column_name: str) -> int:
        column_name_lower = column_name.strip().lower()
        names = [name.strip().lower() for name in self.headers.all_text_contents()]
        if column_name_lower not in names:
            raise ValueError(f"Колонка {column_name!r} не найдена. Есть: {names}")
        return names.index(column_name_lower)

    def row_by_text(self, text: str) -> Locator:
        return self.rows.filter(has_text=text)

    def cell(self, row_text: str, column_name: str) -> Locator:
        index = self.column_index(column_name)
        return self.row_by_text(row_text).locator("td").nth(index)