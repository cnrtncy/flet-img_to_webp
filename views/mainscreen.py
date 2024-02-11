import flet as ft
from PIL import Image
import re
from libs.components.buttons import Button, ButtonIcon
from libs.components.image_item import ImageItem


class MainScreen(ft.UserControl):
    def __init__(self):
        super().__init__()

        # SELECT FILE SECTION
        self.select_files_dialog = ft.FilePicker(on_result=self.select_files_on_result)
        self.select_files_button = ButtonIcon(
            icon=ft.icons.FILE_UPLOAD,
            on_click=self.select_files_open_dialog,
        )
        self.select_files_text = ft.Text(
            value="Select Files",
            width=250,
            size=12,
        )

        # EXTRACT FOLDER SECTION
        self.extract_folder_dialog = ft.FilePicker(
            on_result=self.extract_folder_on_result
        )
        self.extract_folder_button = ButtonIcon(
            icon=ft.icons.FILE_DOWNLOAD, on_click=self.extract_folder_open_dialog
        )

        self.extract_folder_text = ft.TextField(
            disabled=True,
            label="Select Extract Folder",
            label_style=ft.TextStyle(size=13),
            content_padding=10,
            width=250,
            height=40,
            text_size=12,
        )

        # QUALITY SECTION
        self.quality_text = ft.Text("Quality:")
        self.quality_slider = ft.Slider(
            min=0,
            max=100,
            value=70,
            divisions=10,
            label="{value}%",
            on_change_end=self.quality_on_change_end,
        )

        self.convert_button = Button(
            text="CONVERT",
            width=200,
            height=50,
            color="green500",
            on_click=self.convert,
        )
        # CONVERT BUTTON

        self.alert = ft.Text("", color="red300", size=13)

        # FILE LIST SECTION
        self.file_list_checkbox = ft.Checkbox(
            value=True, on_change=self.file_list_checkbox_all
        )
        self.file_list_delete_button = Button(
            text="Delete",
            icon=ft.icons.DELETE_OUTLINE,
            width=120,
            height=30,
            icon_color="red",
            on_click=self.file_list_delete_selected,
        )
        self.file_list = ft.ListView(
            expand=True, spacing=10, padding=20, auto_scroll=True
        )

    def select_files_open_dialog(self, e):
        self.select_files_dialog.pick_files(
            allow_multiple=True, allowed_extensions=["jpg", "png", "jpeg"]
        )

    def select_files_on_result(self, e):
        for i in range(len(e.files)):
            self.file_list.controls.append(
                ImageItem(
                    id=i,
                    name=e.files[i].name,
                    size=e.files[i].size,
                    path=e.files[i].path,
                )
            )
        self.select_files_update()

    def select_files_update(self):
        self.select_files_text.value = (
            f"{len([x for x in self.file_list.controls])} File(s) Included"
        )
        self.update()

    def extract_folder_open_dialog(self, e):
        self.extract_folder_dialog.get_directory_path()

    def extract_folder_on_result(self, e):
        self.extract_folder_text.value = f"{e.path}"
        self.update()

    def quality_on_change_end(self, e):
        if self.quality_slider.value < 60:
            self.alert.value = "Decreasing the value might affect the image quality."
        else:
            self.alert.value = None
        self.update()

    def file_list_checkbox_all(self, e):
        for i in self.file_list.controls:
            if e.control.value == False:
                i.checkbox.value = False
                i.update()
            else:
                i.checkbox.value = True
                i.update()

    def file_list_delete_selected(self, e):
        self.file_list.controls = [
            x for x in self.file_list.controls if x.checkbox.value == False
        ]
        self.update()
        self.select_files_update()

    def convert(self, e):

        convertable_file_list = [
            x for x in self.file_list.controls if x.checkbox.value == True
        ]
        quality = self.quality_slider.value
        extract_folder = self.extract_folder_text.value
        if convertable_file_list and extract_folder:
            for i in convertable_file_list:
                image_file_name = re.sub(f"(.jpg|.jpeg|.png)", "", i.name.value)
                image = Image.open(i.path)
                image = image.convert("RGB")

                image.save(
                    f"{extract_folder}/{image_file_name}.webp",
                    "webp",
                    optimize=True,
                    quality=quality,
                )
            self.alert.value = "All files converted succesfully!"
            self.alert.color = "green500"
            self.file_list.controls = []
            self.extract_folder_text.value = ""
            self.select_files_update()
            self.update()
        else:
            self.alert.value = "You must select Files and Folder Path"
            self.update()

    def build(self):
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Container(
                            width=500,
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            self.select_files_dialog,
                                            self.select_files_button,
                                            self.select_files_text,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            self.extract_folder_dialog,
                                            self.extract_folder_button,
                                            self.extract_folder_text,
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Row(
                                                [
                                                    self.quality_text,
                                                    self.quality_slider,
                                                ]
                                            ),
                                            self.convert_button,
                                        ]
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            border=ft.border.all(2, "grey800"),
                            border_radius=10,
                            width=500,
                            height=500,
                            content=ft.Column(
                                [
                                    ft.Container(
                                        padding=ft.padding.symmetric(5, 20),
                                        border=ft.border.only(
                                            bottom=ft.BorderSide(
                                                width=1, color="grey800"
                                            )
                                        ),
                                        content=ft.Row(
                                            [
                                                self.file_list_checkbox,
                                                self.file_list_delete_button,
                                            ]
                                        ),
                                    ),
                                    self.file_list,
                                ],
                                expand=True,
                            ),
                        ),
                        self.alert,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
