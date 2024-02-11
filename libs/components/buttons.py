import flet as ft


class ButtonIcon(ft.UserControl):
    def __init__(self, icon, on_click=None):
        super().__init__()

        self.button = ft.IconButton(
            icon=icon,
            height=40,
            bgcolor="grey700",
            on_click=on_click,
        )

    def build(self):
        return self.button


class Button(ft.UserControl):
    def __init__(
        self,
        text,
        width=100,
        height=40,
        color="blue",
        icon=None,
        icon_color=None,
        on_click=None,
    ):
        super().__init__()

        self.button = ft.ElevatedButton(
            text=text,
            width=width,
            height=height,
            color=color,
            icon=icon,
            icon_color=icon_color,
            on_click=on_click,
        )

    def build(self):
        return self.button
