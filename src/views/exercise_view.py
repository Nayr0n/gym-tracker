import flet as ft
from models import Exercise
from style import *


class ExerciseView:
    def __init__(self, page: ft.Page, all_exercises: list,
                 selected: list, sets_data: dict, on_exercise_added):
        self.page              = page
        self.all_exercises     = all_exercises
        self.selected          = selected
        self.sets_data         = sets_data
        self.on_exercise_added = on_exercise_added

    # ── Set row ───────────────────────────────────────────────────────────────
    def _make_set_row(self, ex: Exercise, idx: int) -> ft.Control:
        w_field = input_number("0")
        r_field = input_number("0")
        self.sets_data.setdefault(ex.id, []).append(
            {"weight": w_field, "reps": r_field})

        return ft.Row(
            spacing=6,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(width=32, alignment=ft.Alignment(0, 0),
                             content=text_label(str(idx),
                                                text_align=ft.TextAlign.CENTER)),
                ft.Container(expand=1, content=w_field),
                ft.Container(width=24, alignment=ft.Alignment(0, 0),
                             content=text_label("x",
                                                text_align=ft.TextAlign.CENTER)),
                ft.Container(expand=1, content=r_field),
            ],
        )

    # ── Exercise block (card with sets) ───────────────────────────────────────
    def make_exercise_block(self, ex: Exercise) -> ft.Control:
        set_col   = ft.Column(spacing=6)
        set_count = {"n": 1}

        set_col.controls.append(
            ft.Row(spacing=6, controls=[
                ft.Container(width=32,
                             content=text_label("Set",
                                                text_align=ft.TextAlign.CENTER)),
                ft.Container(expand=1,
                             content=text_label("Weight",
                                                text_align=ft.TextAlign.CENTER)),
                ft.Container(width=24),
                ft.Container(expand=1,
                             content=text_label("Reps",
                                                text_align=ft.TextAlign.CENTER)),
            ])
        )
        set_col.controls.append(self._make_set_row(ex, 1))
        set_count["n"] = 2

        def add_set(e):
            set_col.controls.append(self._make_set_row(ex, set_count["n"]))
            set_count["n"] += 1
            set_col.update()

        return card(
            ft.Column(spacing=10, controls=[
                text_heading(ex.name),
                set_col,
                btn_secondary("+ set", on_click=add_set),
            ])
        )

    # ── Exercise picker screen ────────────────────────────────────────────────
    def show_picker(self, exercise_col: ft.Column):
        search_results = ft.Column(
            spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
        pending = set(ex.id for ex in self.selected)

        def refresh_list(query=""):
            search_results.controls.clear()
            q = query.lower()
            for ex in self.all_exercises:
                if q and q not in ex.name.lower():
                    continue

                def toggle(e, eid=ex.id):
                    pending.discard(eid) if eid in pending \
                        else pending.add(eid)
                    refresh_list(search_field.value or "")

                search_results.controls.append(
                    ft.Container(
                        padding=ft.padding.symmetric(vertical=2),
                        content=ft.ListTile(
                            title=text_body(ex.name),
                            subtitle=text_caption(ex.muscle_group),
                            trailing=ft.Icon(
                                ft.Icons.CHECK_CIRCLE_ROUNDED
                                if ex.id in pending
                                else ft.Icons.RADIO_BUTTON_UNCHECKED_ROUNDED,
                                color=ACCENT if ex.id in pending else BORDER,
                                size=20,
                            ),
                            on_click=toggle,
                            bgcolor=CARD if ex.id in pending else BG,
                        ),
                    )
                )
            search_results.update()

        search_field = input_field(
            "Search",
            on_change=lambda e: refresh_list(e.control.value),
        )

        def on_done(e):
            for ex in self.all_exercises:
                if ex.id in pending and ex not in self.selected:
                    self.selected.append(ex)
                    exercise_col.controls.append(self.make_exercise_block(ex))
                    self.on_exercise_added(ex)
            exercise_col.update()
            if picker in self.page.overlay:
                self.page.overlay.remove(picker)
            self.page.update()

        picker = ft.Container(
            expand=True, bgcolor=BG,
            content=ft.Column(
                expand=True, spacing=0,
                controls=[
                    ft.Container(
                        padding=ft.padding.only(
                            left=20, right=20, top=52, bottom=16),
                        content=search_field,
                    ),
                    ft.Container(
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=20),
                        content=search_results,
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(
                            horizontal=20, vertical=16),
                        content=btn_primary("Done", on_click=on_done),
                    ),
                ],
            ),
        )

        self.page.overlay.append(picker)
        self.page.update()
        refresh_list()
