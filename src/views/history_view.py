import flet as ft
from database import Database


class HistoryView:
    def __init__(self, page: ft.Page, db: Database):
        self.page = page
        self.db = db
        self.list_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)

    def build(self):
        self._render()
        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.AppBar(title=ft.Text("History")),
                    self.list_column,
                ],
            ),
        )

    def _render(self):
        self.list_column.controls.clear()
        workouts = self.db.get_workouts()

        if not workouts:
            self.list_column.controls.append(ft.Text("Тренувань ще немає", color=ft.Colors.GREY))
            return

        for w in workouts:
            total_sets = sum(len(ex.sets) for ex in w.exercises)

            def on_open(e, workout=w):
                from views.history_details_view import HistoryDetailsView
                view = HistoryDetailsView(self.page, self.db, workout, on_back=self._on_back)
                self.page.views.append(view.build())
                self.page.update()

            self.list_column.controls.append(
                ft.CupertinoButton(
                    content=ft.Row([
                        ft.Column(
                            [
                                ft.Text(w.name, weight=ft.FontWeight.W_600),
                                ft.Text(f"{w.date}  ·  {len(w.exercises)} вправ  ·  {total_sets} підходів",
                                        color=ft.Colors.GREY, size=12),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT),
                    ]),
                    on_click=on_open,
                    width=999,
                )
            )

    def _on_back(self):
        self._render()
        self.page.update()