import flet as ft
from database import Database
from views.workout_details_view import WorkoutDetailsView
from views.workouts_view import WorkoutsView
from views.history_view import HistoryView
from views.stats_view import StatsView

def main(page: ft.Page):
    db = Database("workout.db")

    page.title   = "Gym Tracker"
    page.padding = 0
    page.spacing = 0

    if page.platform not in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
        page.window.width  = 400
        page.window.height = 750

    NAV_KEYS = ["history", "workout", "stats"]
    content_area = ft.Container(content=WorkoutsView(page, db).build(), expand=True)

    def build_view(key):
        if key == "workout":
            return WorkoutsView(page, db).build()
        elif key == "history":
            return HistoryView(page, db).build()
        elif key == "stats":
            return StatsView(page, db).build()

    def on_nav_change(e):
        key = NAV_KEYS[e.control.selected_index]
        content_area.content = build_view(key)
        page.update()

    def route_change(e):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                padding=0,
                controls=[content_area],
                navigation_bar=ft.CupertinoNavigationBar(
                    selected_index=1,
                    on_change=on_nav_change,
                    destinations=[
                        ft.NavigationBarDestination(icon=ft.Icons.HISTORY,        label="History"),
                        ft.NavigationBarDestination(icon=ft.Icons.FITNESS_CENTER,  label="Workout"),
                        ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART,      label="Stats"),
                    ],
                ),
            )
        )

        if page.route == "/workout-details":
            page.views.append(WorkoutDetailsView(page, db).build())

        page.update()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change(None)

ft.app(target=main)