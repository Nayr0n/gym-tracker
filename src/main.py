import flet as ft
from database import Database
from views.workout_view import WorkoutView
from views.history_view import HistoryView
from views.stats_view import StatsView

def main(page: ft.Page):
    db = Database("workout.db")

    page.title      = "Gym Tracker"
    page.padding    = 0
    page.spacing    = 0
    
    if page.platform not in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
        page.window.width  = 400
        page.window.height = 750

    views = {
        "workout": WorkoutView(page, db).build(),
        "history": HistoryView(page, db).build(),
        "stats": StatsView(page, db).build()
    }

    content_area = ft.Container(content=views["workout"],expand=True)

    NAV_KEYS = ["history", "workout", "stats"]

    def on_nav_change(e):
        selected_key = NAV_KEYS[e.control.selected_index]
        content_area.content = views[selected_key]
        page.update()

    page.navigation_bar = ft.CupertinoNavigationBar(
        selected_index=1,
        on_change=on_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY,label="History",),
            ft.NavigationBarDestination(icon=ft.Icons.FITNESS_CENTER, label="Workout",),
            ft.NavigationBarDestination(icon=ft.Icons.BAR_CHART,label="Stats",),
        ],
    )

    page.add(content_area)

ft.app(target=main)