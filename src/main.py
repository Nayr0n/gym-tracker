import flet as ft
from views.home_view import HomeView
from views.history_view import HistoryView
from views.stats_view import StatsView
from database import Database
from style import *


def main(page: ft.Page):
    db = Database("workout.db")

    page.title       = "Gym Tracker"
    page.theme_mode  = ft.ThemeMode.DARK
    page.bgcolor     = BG
    page.padding     = 0
    
    if not page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]:
        page.window.width = 400
        page.window.height = 750

    home_view    = HomeView(page, db)
    history_view = HistoryView(page, db)
    stats_view   = StatsView(page, db)

    views = {
        "home":    home_view.build(),
        "history": history_view.build(),
        "stats":   stats_view.build(),
    }

    content_area = ft.Container(expand=True)

    def switch_tab(key: str):
        content_area.content = views[key]
        for btn in nav_row.controls:
            btn.style.color = ACCENT if btn.data == key else SUBTEXT
        page.update()

    def make_nav_btn(icon, label, key):
        return ft.TextButton(
            data=key,
            on_click=lambda e: switch_tab(e.control.data),
            style=ft.ButtonStyle(
                color=ACCENT if key == "home" else SUBTEXT,
                overlay_color=ft.Colors.with_opacity(0.05, ACCENT),
                padding=ft.padding.symmetric(horizontal=16, vertical=8),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Icon(icon, size=22),
                    ft.Text(label, size=10, weight=ft.FontWeight.W_600,
                            style=ft.TextStyle(letter_spacing=1.5)),
                ],
            ),
        )

    nav_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            make_nav_btn(ft.Icons.HISTORY_ROUNDED,        "History", "history"),
            make_nav_btn(ft.Icons.FITNESS_CENTER_ROUNDED, "Workout", "home"),
            make_nav_btn(ft.Icons.BAR_CHART_ROUNDED,      "Stats",   "stats"),
        ],
    )

    nav_bar = ft.Container(
        content=nav_row,
        bgcolor=SURFACE,
        border=ft.border.only(top=ft.BorderSide(0.5, BORDER)),
        padding=ft.padding.symmetric(vertical=10),
    )

    content_area.content = views["home"]

    page.add(
        ft.Column(
            expand=True, spacing=0,
            controls=[
                ft.Container(content=content_area, expand=True),
                nav_bar,
            ],
        )
    )


ft.app(target=main)
