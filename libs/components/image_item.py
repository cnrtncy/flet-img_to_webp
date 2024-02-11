import flet as ft


class ImageItem(ft.UserControl):
    def __init__(self, id: int, name: str, size: int, path: str) -> ft.Container:
        super().__init__()

        self.id = id
        self.checkbox = ft.Checkbox(value=True)
        self.name = ft.Text(name)
        self.path = path
        self.size = ft.Text(
            f"{size / 1000:.2f}KB",
            size=14,
        )
        self.new_size = ft.Text(f"{size}KB", visible=False)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def build(self):
        return ft.Container(
            content=ft.Row(
                [self.checkbox, self.name, ft.Row([self.size, self.new_size])],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
