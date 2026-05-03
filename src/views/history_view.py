import flet as ft
from database import Database
from datetime import datetime
from style import *


def _fmt_date(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso).strftime("%d %b %Y")
    except Exception:
        return iso

def _fmt_time(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso).strftime("%H:%M")
    except Exception:
        return ""


class HistoryView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db   = db

    def build(self) -> ft.Control:
        workouts = sorted(
            self.db.get_workouts(), key=lambda w: w.date, reverse=True)

        if not workouts:
            return ft.Container(
                expand=True, bgcolor=BG,
                alignment=ft.Alignment(0, 0),
                content=text_caption("No workouts yet"),
            )

        list_col = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

        def rebuild():
            ws = sorted(self.db.get_workouts(),
                        key=lambda w: w.date, reverse=True)
            list_col.controls = [make_row(w) for w in ws]
            list_col.update()

        # ── Detail overlay ────────────────────────────────────────────────────
        def show_detail(w):
            rows = []
            for ex in w.exercises:
                set_rows = [
                    ft.Row(spacing=12, controls=[
                        text_caption(f"Set {i+1}"),
                        text_body(f"{s.weight} kg  ×  {s.reps}"),
                    ])
                    for i, s in enumerate(ex.sets)
                ]
                rows.append(card(ft.Column(spacing=8, controls=[
                    text_heading(ex.name), *set_rows,
                ])))

            detail = ft.Container(
                expand=True, bgcolor=BG,
                content=ft.Column(
                    expand=True, spacing=0,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(
                                left=20, right=20, top=52, bottom=16),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Column(spacing=2, controls=[
                                        text_heading(_fmt_date(w.date)),
                                        text_caption(_fmt_time(w.date)),
                                    ]),
                                    ft.IconButton(
                                        ft.Icons.CLOSE_ROUNDED,
                                        icon_color=SUBTEXT, icon_size=20,
                                        on_click=lambda e, d=None: close_overlay(),
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            padding=ft.padding.symmetric(horizontal=20),
                            content=ft.Column(
                                expand=True, scroll=ft.ScrollMode.AUTO,
                                spacing=0,
                                controls=[*rows, ft.Container(height=20)],
                            ),
                        ),
                    ],
                ),
            )

            self._current_overlay = detail
            self.page.overlay.append(detail)
            self.page.update()

        def close_overlay():
            if hasattr(self, "_current_overlay") and \
               self._current_overlay in self.page.overlay:
                self.page.overlay.remove(self._current_overlay)
            self.page.update()

        # ── Edit overlay ──────────────────────────────────────────────────────
        def show_edit(w):
            date_field = input_field(
                "Date", ref=None,
                height=44,
            )
            date_field.value = _fmt_date(w.date)

            def save_edit(e):
                # оновлюємо дату в БД напряму
                try:
                    new_dt = datetime.strptime(
                        date_field.value.strip(), "%d %b %Y")
                    cursor = self.db.conn.cursor()
                    cursor.execute(
                        "UPDATE workouts SET date=? WHERE id=?",
                        (new_dt.isoformat(), w.id))
                    self.db.conn.commit()
                except Exception:
                    pass
                close_overlay()
                rebuild()

            edit = ft.Container(
                expand=True, bgcolor=BG,
                content=ft.Column(
                    expand=True, spacing=0,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(
                                left=20, right=20, top=52, bottom=16),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    text_heading("Edit workout"),
                                    ft.IconButton(
                                        ft.Icons.CLOSE_ROUNDED,
                                        icon_color=SUBTEXT, icon_size=20,
                                        on_click=lambda e: close_overlay(),
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            padding=ft.padding.symmetric(horizontal=20),
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    text_label("DATE  (DD Mon YYYY)"),
                                    date_field,
                                    ft.Container(height=8),
                                    btn_primary("Save", on_click=save_edit),
                                ],
                            ),
                        ),
                    ],
                ),
            )

            self._current_overlay = edit
            self.page.overlay.append(edit)
            self.page.update()

        # ── Dismissible row ───────────────────────────────────────────────────
        def make_row(w):
            ex_names = ", ".join(ex.name for ex in w.exercises) or "—"

            tile = ft.ListTile(
                title=text_body(_fmt_date(w.date)),
                subtitle=text_caption(ex_names),
                trailing=ft.Icon(
                    ft.Icons.CHEVRON_RIGHT_ROUNDED,
                    size=18, color=SUBTEXT,
                ),
                on_click=lambda e, workout=w: show_detail(workout),
            )

            # фон при свайпі вліво — видалення (червоний)
            bg_delete = ft.Container(
                bgcolor=ft.Colors.with_opacity(0.15, "#FF4444"),
                padding=ft.padding.only(right=20),
                alignment=ft.Alignment(1, 0),
                content=ft.Row(spacing=6, controls=[
                    ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED,
                            color="#FF4444", size=20),
                    text_caption("Delete"),
                ]),
            )

            # фон при свайпі вправо — редагування (акцент)
            bg_edit = ft.Container(
                bgcolor=ft.Colors.with_opacity(0.1, ACCENT),
                padding=ft.padding.only(left=20),
                alignment=ft.Alignment(-1, 0),
                content=ft.Row(spacing=6, controls=[
                    ft.Icon(ft.Icons.EDIT_OUTLINED,
                            color=ACCENT, size=20),
                    text_caption("Edit"),
                ]),
            )

            def on_dismiss(e, workout=w):
                direction = e.direction
                if direction == ft.DismissDirection.END_TO_START:
                    # видалити з БД
                    cursor = self.db.conn.cursor()
                    cursor.execute(
                        "DELETE FROM sets WHERE workout_id=?", (workout.id,))
                    cursor.execute(
                        "DELETE FROM workouts WHERE id=?", (workout.id,))
                    self.db.conn.commit()
                    rebuild()
                elif direction == ft.DismissDirection.START_TO_END:
                    # відкрити редагування — спочатку повертаємо елемент
                    rebuild()
                    show_edit(workout)

            return ft.Dismissible(
                key=str(w.id),
                content=tile,
                background=bg_edit,
                secondary_background=bg_delete,
                dismiss_direction=ft.DismissDirection.HORIZONTAL,
                dismiss_thresholds={
                    ft.DismissDirection.START_TO_END: 0.3,
                    ft.DismissDirection.END_TO_START: 0.3,
                },
                on_dismiss=on_dismiss,
            )

        list_col.controls = [make_row(w) for w in workouts]

        return ft.Container(
            expand=True, bgcolor=BG,
            content=ft.Column(
                expand=True, spacing=0,
                controls=[
                    ft.Container(height=52),
                    ft.Container(
                        expand=True,
                        content=list_col,
                    ),
                ],
            ),
        )
