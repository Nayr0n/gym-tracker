import flet as ft
from database import Database
from models import Set
from views.exercises_view import ExercisesView


class HistoryDetailsView:
    def __init__(self, page: ft.Page, db: Database, workout, on_back):
        self.page = page
        self.db = db
        self.workout = workout
        self.on_back = on_back

    def build(self):
        self.exercises_column = ft.Column(spacing=16)
        self._render()

        def on_save(e):
            self.db.update_workout(self.workout)
            self.page.views.pop()
            self.page.update()
            self.on_back()

        def on_delete(e):
            def confirm(e):
                dlg.open = False
                self.db.delete_workout(self.workout.id)
                self.page.views.pop()
                self.page.update()
                self.on_back()

            def cancel(e):
                dlg.open = False
                self.page.update()

            dlg = ft.AlertDialog(
                title=ft.Text("Видалити тренування?"),
                actions=[
                    ft.TextButton("Скасувати", on_click=cancel),
                    ft.TextButton("Видалити", on_click=confirm),
                ],
            )

            self.page.overlay.append(dlg)
            dlg.open = True
            self.page.update()

        return ft.View(
            route="/history-details",
            controls=[
                ft.AppBar(
                    leading=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: (self.page.views.pop(), self.page.update()),
                    ),
                    title=ft.TextField(
                        value=self.workout.name,
                        border=ft.InputBorder.NONE,
                        on_change=lambda e: setattr(self.workout, "name", e.control.value),
                    ),
                    actions=[
                        ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, on_click=on_delete),
                    ],
                ),
                ft.Column(
                    expand=True,
                    controls=[self.exercises_column],
                    scroll=ft.ScrollMode.AUTO,
                ),
                ft.CupertinoButton(content=ft.Text("Save"), on_click=on_save, width=999),
            ],
        )

    def _render(self):
        self.exercises_column.controls.clear()

        for ex in self.workout.exercises:
            self.exercises_column.controls.append(self._exercise_block(ex))

        self.exercises_column.controls.append(
            ft.CupertinoButton(content=ft.Text("+ exercise"), on_click=self._open_exercises, width=999)
        )

    def _exercise_block(self, ex):
        table = ft.Column(spacing=4)

        def refresh():
            table.controls.clear()
            table.controls.append(ft.Row([
                ft.Text("Set",    expand=1, color=ft.Colors.GREY),
                ft.Text("Weight", expand=2, color=ft.Colors.GREY),
                ft.Text("x",      width=20),
                ft.Text("Reps",   expand=2, color=ft.Colors.GREY),
            ]))

            for i, s in enumerate(ex.sets):
                def on_w(e, s=s):
                    v = e.control.value.strip()
                    if not v:
                        ex.sets.remove(s)
                        refresh()
                        self.page.update()
                    else:
                        try: s.weight = float(v)
                        except: pass

                def on_r(e, s=s):
                    v = e.control.value.strip()
                    if not v:
                        ex.sets.remove(s)
                        refresh()
                        self.page.update()
                    else:
                        try: s.reps = int(v)
                        except: pass

                table.controls.append(ft.Row([
                    ft.Text(str(i + 1), expand=1),
                    ft.TextField(value=str(s.weight), expand=2, height=40, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER, on_change=on_w),
                    ft.Text("x", width=20),
                    ft.TextField(value=str(s.reps), expand=2, height=40, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER, on_change=on_r),
                ]))

            nw = ft.TextField(expand=2, height=40, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
            nr = ft.TextField(expand=2, height=40, text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)

            def try_add(e):
                w_val = nw.value.strip() if nw.value else ""
                r_val = nr.value.strip() if nr.value else ""
                if w_val and r_val:
                    try:
                        ex.sets.append(Set(
                            workout_id=self.workout.id, exercise_id=ex.id or 0,
                            status="done", weight=float(w_val), reps=int(r_val), rest_time=60,
                        ))
                        refresh()
                        self.page.update()
                    except: pass

            nw.on_blur = try_add
            nr.on_blur = try_add

            table.controls.append(ft.Row([
                ft.Text(str(len(ex.sets) + 1), expand=1, color=ft.Colors.GREY),
                nw, ft.Text("x", width=20), nr,
            ]))

        refresh()
        return ft.Column(spacing=8, controls=[ft.Text(ex.name, weight=ft.FontWeight.W_600), table])

    def _open_exercises(self, e):
        from models import Exercise

        def on_pick(exercises):
            for exercise in exercises:
                self.workout.exercises.append(Exercise(
                    id=exercise.id, name=exercise.name, description=exercise.description,
                    img=exercise.img, muscle_group=exercise.muscle_group, sets=[],
                ))
            self._render()
            self.page.update()

        self.page.views.append(ExercisesView(self.page, self.db, on_pick=on_pick).build())
        self.page.update()