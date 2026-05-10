import flet as ft
from database import Database


class HistoryView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db = db

    def build(self):
        workouts = self.db.get_workouts()

        rows = []
        for w in workouts:
            rows.append(ft.Text(f"{w.date} — {w.name}"))

        if not rows:
            rows.append(ft.Text("Тренувань ще немає"))

        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.AppBar(title=ft.Text("History")),
                    *rows,
                ],
            ),
        )