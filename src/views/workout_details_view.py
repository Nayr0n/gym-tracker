import flet as ft
from database import Database

class WorkoutDetailsView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db   = db

    def build(self):
        def go_back(e):
            self.page.go("/")
 
        return ft.View(
            route="/workout-details",
            controls=[
                ft.AppBar(
                    leading=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=go_back,
                    ),
                    title=ft.Text("Workout details"),
                ),
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            ft.Text("Exercise details will go here..."),
                        ],
                    ),
                ),
            ],
        )