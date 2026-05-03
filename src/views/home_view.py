import flet as ft
from database import Database
from views.workout_view import WorkoutView
from style import *


class HomeView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db   = db

    def build(self) -> ft.Control:
        exercises = self.db.get_all_exercises()

        def start_workout(e):
            wv = WorkoutView(self.page, self.db, exercises, on_done=lambda: None)
            self.page.overlay.append(wv.build())
            self.page.update()

        return ft.Container(
            expand=True,
            bgcolor=BG,
            padding=ft.padding.only(left=24, right=24, top=52),
            content=ft.Column(
                expand=True,
                controls=[
                    btn_secondary("+ start workout", on_click=start_workout),
                    ft.Container(expand=True),
                ],
            ),
        )
