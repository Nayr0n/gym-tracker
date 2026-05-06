import flet as ft

# Colors 
BACKGROUND = "#0D0D0D"
SURFACE = "#161616"
CARD    = "#1C1C1C"
BORDER  = "#2A2A2A"
ACCENT  = "#4762E8"
TEXT    = "#F0F0F0"
SUBTEXT = "#666666"

# Text
def text_title(value: str):
    return ft.Text(
        value, 
        size=28, 
        weight=ft.FontWeight.W_900, 
        color=TEXT, 
        style=ft.TextStyle(letter_spacing=2)
    )

def text_body(value: str):
    return ft.Text(
        value, 
        size=16, 
        color=TEXT
        )

def text_label(value: str):
    return ft.Text(
        value.upper(), 
        size=12, 
        weight=ft.FontWeight.W_600, 
        color=SUBTEXT, 
        style=ft.TextStyle(letter_spacing=1.5)
    )

def text_caption(value: str):
    return ft.Text(
        value, 
        size=12, 
        color=SUBTEXT
    )

# Buttons
def btn_primary(text: str, on_click, icon=None, expand=False):
    return ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(icon, size=20) if icon else ft.Container(), 
                ft.Text(text, size=14, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            tight=True
        ),
        bgcolor=ACCENT,
        color=BACKGROUND,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(vertical=18, horizontal=20),
            overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        ),
        on_click=on_click,
        expand=expand
    )

def btn_secondary(text: str, on_click, icon=None, expand=False):
    return ft.OutlinedButton(
        content=ft.Row(
            [
                ft.Icon(icon, size=18) if icon else ft.Container(), 
                ft.Text(text, size=14, weight=ft.FontWeight.W_600)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            tight=True
        ),
        style=ft.ButtonStyle(
            color=TEXT,
            side=ft.BorderSide(1, BORDER),
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(vertical=18, horizontal=20),
        ),
        on_click=on_click,
        expand=expand
    )

def btn_ghost(text: str, on_click, icon=None):
    return ft.TextButton(
        content=ft.Row(
            [
                ft.Icon(icon, size=16) if icon else ft.Container(),
                ft.Text(text, size=13, weight=ft.FontWeight.W_500)
            ],
            tight=True
        ),
        style=ft.ButtonStyle(
            color=SUBTEXT,
            padding=ft.padding.all(10),
        ),
        on_click=on_click
    )

# Containers
def card(content, padding=16, on_click=None):
    return ft.Container(
        content=content,
        bgcolor=SURFACE,
        border_radius=12,
        border=ft.border.all(1, BORDER),
        padding=padding,
        on_click=on_click,
        ink=True if on_click else False,
    )

def page_container(content):
    return ft.Container(
        content=content,
        expand=True,
        padding=ft.padding.only(left=20, right=20, top=10, bottom=10),
    )

def sticky_bottom(content):
    return ft.Container(
        content=content,
        padding=ft.padding.all(20),
        bgcolor=BACKGROUND,
        border=ft.border.only(top=ft.BorderSide(1, BORDER)),
    )

