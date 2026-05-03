import flet as ft
from models import Exercise
from style import *


class ExerciseRow:
    def __init__(self, exercise: Exercise, on_tap=None):
        self.exercise = exercise
        self.on_tap   = on_tap

    def build(self) -> ft.Control:
        ex    = self.exercise
        color = MUSCLE_COLORS.get(ex.muscle_group.lower(), SUBTEXT)

        chip = ft.Container(
            padding=ft.padding.symmetric(horizontal=8, vertical=3),
            border_radius=3,
            border=ft.border.all(1, ft.Colors.with_opacity(0.35, color)),
            bgcolor=ft.Colors.with_opacity(0.08, color),
            content=ft.Text(ex.muscle_group.upper(), size=8, color=color,
                            style=ft.TextStyle(letter_spacing=1.5)),
        )

        icon_box = ft.Container(
            width=42, height=42,
            border_radius=8,
            bgcolor=SURFACE,
            border=ft.border.all(1, BORDER),
            content=ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED,
                            size=20, color=SUBTEXT),
            alignment=ft.Alignment(0, 0),
        )

        def _tap(e):
            if self.on_tap:
                self.on_tap(ex)

        return ft.Container(
            on_click=_tap,
            margin=ft.margin.only(bottom=8),
            padding=ft.padding.all(16),
            bgcolor=CARD,
            border_radius=8,
            border=ft.border.all(1, BORDER),
            ink=True,
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    icon_box,
                    ft.Container(width=14),
                    ft.Column(
                        expand=True, spacing=4,
                        controls=[
                            ft.Text(ex.name, size=13,
                                    weight=ft.FontWeight.W_600, color=TEXT),
                            chip,
                        ],
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED,
                            size=18, color=BORDER),
                ],
            ),
        )
