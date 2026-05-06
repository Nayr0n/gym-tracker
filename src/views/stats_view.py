import flet as ft

class StatsView:
    def __init__(self, page: ft.Page, db):
        self.page = page
        self.db = db

    def build(self):
        # Поки що просто повертаємо заголовок
        return ft.Container(
            content=ft.Column([ft.Text("STATS")])
        )