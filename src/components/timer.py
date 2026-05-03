import flet as ft
import threading
import time
from style import *


class WorkoutTimer:
    def __init__(self):
        self._seconds = 0
        self._running = False
        self._ref     = ft.Ref()

    def start(self):
        if self._running:
            return
        self._running = True
        threading.Thread(target=self._tick, daemon=True).start()

    def stop(self):
        self._running = False

    def reset(self):
        self.stop()
        self._seconds = 0
        self._update_display()

    @property
    def seconds(self) -> int:
        return self._seconds

    def _tick(self):
        while self._running:
            time.sleep(1)
            self._seconds += 1
            self._update_display()

    def _update_display(self):
        if self._ref.current:
            self._ref.current.value = self._fmt()
            try:
                self._ref.current.update()
            except Exception:
                self._running = False

    def _fmt(self) -> str:
        m, s = divmod(self._seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

    def build(self) -> ft.Control:
        return ft.Text(
            ref=self._ref,
            value=self._fmt(),
            size=22,
            weight=ft.FontWeight.W_700,
            color=TEXT,
            style=ft.TextStyle(letter_spacing=3),
        )
