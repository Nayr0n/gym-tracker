import flet as ft
from database import Database
from models import Workout, Exercise, Set
from datetime import datetime
import threading, time
from style import *
from views.exercise_view import ExerciseView


class WorkoutView:
    def __init__(self, page: ft.Page, db: Database,
                 exercises: list, on_done):
        self.page           = page
        self.db             = db
        self.on_done        = on_done
        self.selected       = []
        self.sets_data      = {}
        self._overlay_ref   = None

        self.exercise_view = ExerciseView(
            page=page,
            all_exercises=exercises,
            selected=self.selected,
            sets_data=self.sets_data,
            on_exercise_added=lambda ex: None,
        )

    # ── Close / Finish ────────────────────────────────────────────────────────
    def _close(self):
        if self._overlay_ref and self._overlay_ref in self.page.overlay:
            self.page.overlay.remove(self._overlay_ref)
        self.page.update()
        self.on_done()

    def _finish(self, e):
        exercises_out = []
        for ex in self.selected:
            sets = [
                Set(
                    workout_id=0, exercise_id=ex.id, status="done",
                    reps=int(row["reps"].value or 0),
                    weight=float(row["weight"].value or 0),
                    rest_time=60,
                )
                for row in self.sets_data.get(ex.id, [])
            ]
            exercises_out.append(Exercise(
                id=ex.id, name=ex.name, description=ex.description,
                img=ex.img, muscle_group=ex.muscle_group, sets=sets,
            ))
        self.db.save_workout(Workout(
            name="Workout", description="", img="",
            date=datetime.now().isoformat(),
            exercises=exercises_out,
        ))
        self._close()

    # ── Build ─────────────────────────────────────────────────────────────────
    def build(self) -> ft.Control:
        exercise_col = ft.Column(spacing=0)

        body = ft.Container(
            expand=True, bgcolor=BG,
            content=ft.Column(
                expand=True, spacing=0,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(
                            left=20, right=20, top=52, bottom=12),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.IconButton(
                                    ft.Icons.CLOSE_ROUNDED,
                                    icon_color=SUBTEXT, icon_size=20,
                                    on_click=lambda e: self._close(),
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=20),
                        content=ft.Column(
                            expand=True, scroll=ft.ScrollMode.AUTO, spacing=0,
                            controls=[
                                exercise_col,
                                ft.Container(height=8),
                                btn_secondary(
                                    "+ exercise",
                                    on_click=lambda e:
                                        self.exercise_view.show_picker(
                                            exercise_col),
                                ),
                                ft.Container(height=20),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=20, vertical=16),
                        content=btn_secondary(
                            "Finish", on_click=self._finish),
                    ),
                ],
            ),
        )

        self._overlay_ref = body
        return body
