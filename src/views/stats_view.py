import flet as ft
from database import Database
from style import *


class StatsView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db   = db

    def build(self) -> ft.Control:
        workouts = self.db.get_workouts()

        total_workouts = len(workouts)
        total_sets   = sum(len(ex.sets) for w in workouts for ex in w.exercises)
        total_volume = sum(s.reps * s.weight for w in workouts
                           for ex in w.exercises for s in ex.sets)
        total_reps   = sum(s.reps for w in workouts
                           for ex in w.exercises for s in ex.sets)

        muscle_count: dict = {}
        for w in workouts:
            for ex in w.exercises:
                mg = ex.muscle_group.lower()
                muscle_count[mg] = muscle_count.get(mg, 0) + len(ex.sets)

        max_count = max(muscle_count.values()) if muscle_count else 1

        muscle_rows = [
            muscle_bar(mg, cnt, max_count)
            for mg, cnt in sorted(muscle_count.items(), key=lambda x: -x[1])
        ] if muscle_count else [text_caption("No data yet")]

        return ft.Column(
            expand=True, scroll=ft.ScrollMode.AUTO, spacing=0,
            controls=[
                ft.Container(
                    padding=ft.padding.only(left=24, right=24,
                                            top=52, bottom=20),
                    content=text_title("STATS"),
                ),
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=24),
                    content=ft.Column(spacing=10, controls=[
                        ft.Row(spacing=10, controls=[
                            stat_tile(str(total_workouts), "WORKOUTS", ACCENT),
                            stat_tile(str(total_sets), "TOTAL SETS"),
                        ]),
                        ft.Row(spacing=10, controls=[
                            stat_tile(f"{total_volume:,.0f}", "KG VOLUME"),
                            stat_tile(str(total_reps), "TOTAL REPS"),
                        ]),
                    ]),
                ),
                ft.Container(
                    padding=ft.padding.only(left=24, right=24,
                                            top=28, bottom=12),
                    content=text_label("MUSCLE GROUPS"),
                ),
                *[ft.Container(r, padding=ft.padding.symmetric(horizontal=24))
                  for r in muscle_rows],
                ft.Container(height=20),
            ],
        )
