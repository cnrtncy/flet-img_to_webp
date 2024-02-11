import flet as ft
from views.mainscreen import MainScreen


def main(page: ft.Page):
    page.title = "imageTo WEBP"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 600
    page.window_height = 800
    page.window_resizable = False

    page.update()

    page.add(MainScreen())


ft.app(target=main)
