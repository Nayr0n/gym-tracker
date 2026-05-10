import flet as ft
from database import Database


class ExercisesView:
    def __init__(self, page: ft.Page, db: Database, on_pick):
        self.page = page
        self.db = db
        self.on_pick = on_pick  # on_pick(list[Exercise])
        self.selected = []

    def build(self):
        catalog = self.db.get_all_exercises()
        results = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        done_btn = ft.CupertinoButton(
            content=ft.Text("Select"),
            width=999,
            on_click=self._on_done,
        )
        self.done_btn = done_btn

        def on_search(e):
            query = search_field.value.lower() if search_field.value else ""
            results.controls.clear()
            for ex in catalog:
                if query in ex.name.lower():
                    is_selected = any(s.id == ex.id for s in self.selected)

                    def toggle(e, exercise=ex):
                        if any(s.id == exercise.id for s in self.selected):
                            self.selected = [s for s in self.selected if s.id != exercise.id]
                        else:
                            self.selected.append(exercise)
                        self._update_btn()
                        on_search(None)
                        self.page.update()

                    results.controls.append(
                        ft.CupertinoButton(
                            content=ft.Row([
                                ft.Text(ex.name, expand=1),
                                ft.Icon(ft.Icons.CHECK, visible=is_selected),
                            ]),
                            on_click=toggle,
                            width=999,
                        )
                    )
            self.page.update()

        self.on_search = on_search
        search_field = ft.TextField(hint_text="Search", expand=True, on_change=on_search)
        self.search_field = search_field
        on_search(None)

        return ft.View(
            route="/exercises",
            controls=[
                ft.AppBar(title=ft.Text("Вправи")),
                ft.Row([search_field]),
                results,
                done_btn,
            ],
        )

    def _update_btn(self):
        count = len(self.selected)
        self.done_btn.content = ft.Text(f"Select ({count})" if count else "Select")
        self.done_btn.update()

    def _on_done(self, e):
        self.page.views.pop()
        self.page.update()
        if self.selected:
            self.on_pick(self.selected)