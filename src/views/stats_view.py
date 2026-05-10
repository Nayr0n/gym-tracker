import flet as ft
from database import Database


class StatsView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db = db

    def build(self):
        workouts = self.db.get_workouts()

        total_workouts = len(workouts)
        total_sets = sum(len(ex.sets) for w in workouts for ex in w.exercises)
        total_volume = sum(s.reps * s.weight for w in workouts for ex in w.exercises for s in ex.sets)

        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.AppBar(title=ft.Text("Stats")),
                    ft.Text(f"Тренувань: {total_workouts}"),
                    ft.Text(f"Підходів: {total_sets}"),
                    ft.Text(f"Об'єм: {total_volume:.0f} кг"),
                ],
            ),
        )