import flet as ft

# ── Colors ────────────────────────────────────────────────────────────────────
BG      = "#0D0D0D"
SURFACE = "#161616"
CARD    = "#1C1C1C"
BORDER  = "#2A2A2A"
ACCENT  = "#4762E8"
TEXT    = "#F0F0F0"
SUBTEXT = "#666666"

MUSCLE_COLORS = {
    "chest":     "#FF6B35",
    "back":      "#4ECDC4",
    "legs":      "#FFE66D",
    "shoulders": "#A8EDEA",
    "arms":      "#C8FF00",
    "core":      "#FF8B94",
    "cardio":    "#B5EAD7",
}

# ── Text ──────────────────────────────────────────────────────────────────────
def text_title(value: str, **kw) -> ft.Text:
    return ft.Text(value, size=22, weight=ft.FontWeight.W_800,
                   color=TEXT, style=ft.TextStyle(letter_spacing=4), **kw)

def text_heading(value: str, **kw) -> ft.Text:
    return ft.Text(value, size=16, weight=ft.FontWeight.W_600,
                   color=TEXT, **kw)

def text_body(value: str, **kw) -> ft.Text:
    return ft.Text(value, size=14, color=TEXT, **kw)

def text_label(value: str, **kw) -> ft.Text:
    return ft.Text(value, size=10, color=SUBTEXT,
                   style=ft.TextStyle(letter_spacing=1.5), **kw)

def text_caption(value: str, **kw) -> ft.Text:
    return ft.Text(value, size=10, color=SUBTEXT, **kw)

def text_mono(value: str, size=18, color=TEXT,
              letter_spacing=2.0, **kw) -> ft.Text:
    return ft.Text(value, size=size, weight=ft.FontWeight.W_700,
                   color=color,
                   style=ft.TextStyle(letter_spacing=letter_spacing), **kw)

# ── Buttons ───────────────────────────────────────────────────────────────────
def btn_primary(label: str, on_click=None,
                width=99999, ref=None) -> ft.ElevatedButton:
    return ft.ElevatedButton(
        ref=ref,
        content=ft.Text(label, size=14, weight=ft.FontWeight.W_600,
                        color="#0D0D0D"),
        on_click=on_click,
        bgcolor=ACCENT,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            overlay_color=ft.Colors.with_opacity(0.15, "#000000"),
            padding=ft.padding.symmetric(vertical=20),
        ),
        width=width,
    )

def btn_secondary(label: str, on_click=None,
                  width=99999, ref=None) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        ref=ref,
        content=ft.Text(label, size=14, color=TEXT),
        on_click=on_click,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, BORDER),
            shape=ft.RoundedRectangleBorder(radius=8),
            overlay_color=ft.Colors.with_opacity(0.05, TEXT),
            padding=ft.padding.symmetric(vertical=20),
        ),
        width=width,
    )

def btn_ghost(label: str, on_click=None) -> ft.TextButton:
    return ft.TextButton(
        content=ft.Text(label, size=12, color=SUBTEXT),
        on_click=on_click,
        style=ft.ButtonStyle(
            overlay_color=ft.Colors.with_opacity(0.05, TEXT),
            padding=ft.padding.symmetric(vertical=8),
        ),
    )

# ── Inputs ────────────────────────────────────────────────────────────────────
def input_field(hint: str, keyboard_type=ft.KeyboardType.TEXT,
                on_change=None, ref=None, height=44) -> ft.TextField:
    return ft.TextField(
        ref=ref,
        hint_text=hint,
        keyboard_type=keyboard_type,
        border_color=BORDER,
        focused_border_color=ACCENT,
        color=TEXT,
        hint_style=ft.TextStyle(color=SUBTEXT),
        bgcolor=SURFACE,
        border_radius=8,
        height=height,
        content_padding=ft.padding.symmetric(horizontal=14, vertical=0),
        text_size=13,
        on_change=on_change,
    )

def input_number(hint: str = "0", ref=None) -> ft.TextField:
    return ft.TextField(
        ref=ref,
        value="",
        hint_text=hint,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        text_size=13,
        height=36,
        content_padding=4,
        border_color=BORDER,
        focused_border_color=ACCENT,
        color=TEXT,
        hint_style=ft.TextStyle(color=SUBTEXT),
        bgcolor=SURFACE,
        border_radius=6,
    )

# ── Cards / Containers ────────────────────────────────────────────────────────
def card(content: ft.Control, padding=14,
         margin_bottom=12, **kw) -> ft.Container:
    return ft.Container(
        content=content,
        padding=ft.padding.all(padding),
        margin=ft.margin.only(bottom=margin_bottom),
        bgcolor=CARD,
        border_radius=8,
        border=ft.border.all(1, BORDER),
        **kw,
    )

def icon_box(icon, size=20, box_size=42) -> ft.Container:
    return ft.Container(
        width=box_size, height=box_size,
        border_radius=8,
        bgcolor=SURFACE,
        border=ft.border.all(1, BORDER),
        content=ft.Icon(icon, size=size, color=SUBTEXT),
        alignment=ft.Alignment(0, 0),
    )

def muscle_chip(group: str) -> ft.Container:
    color = MUSCLE_COLORS.get(group.lower(), SUBTEXT)
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
        border_radius=3,
        border=ft.border.all(1, ft.Colors.with_opacity(0.35, color)),
        bgcolor=ft.Colors.with_opacity(0.08, color),
        content=ft.Text(group.upper(), size=8, color=color,
                        style=ft.TextStyle(letter_spacing=1.5)),
    )

# ── Stats widgets ─────────────────────────────────────────────────────────────
def stat_tile(value: str, label: str, color=TEXT) -> ft.Container:
    return ft.Container(
        expand=True,
        padding=ft.padding.all(16),
        bgcolor=CARD,
        border_radius=8,
        border=ft.border.all(1, BORDER),
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(value, size=26, weight=ft.FontWeight.W_800,
                        color=color),
                text_label(label),
            ],
        ),
    )

def muscle_bar(mg: str, count: int, max_count: int) -> ft.Container:
    color = MUSCLE_COLORS.get(mg, SUBTEXT)
    pct   = count / max_count if max_count else 0
    return card(
        ft.Column(spacing=8, controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    text_body(mg.upper()),
                    text_caption(f"{count} sets"),
                ],
            ),
            ft.Stack(height=4, controls=[
                ft.Container(height=4, border_radius=2,
                             bgcolor=BORDER, expand=True),
                ft.Container(height=4, border_radius=2,
                             bgcolor=color, expand=True, opacity=pct),
            ]),
        ]),
        margin_bottom=8,
    )
