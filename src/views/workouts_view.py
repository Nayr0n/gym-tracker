import flet as ft
from database import Database


class WorkoutsView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db = db

    def build(self):
        def start_workout(e):
            self.page.go("/workout-details")

        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.AppBar(title=ft.Text("Workout")),
                    ft.Button(
                        content=ft.Text("+ Start Workout"),
                        on_click=start_workout,
                        width=999,
                    ),
                ],
            ),
        )