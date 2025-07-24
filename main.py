import flet as ft

def main(page: ft.Page):
    page.window.frameless = True
    page.window.title_bar_hidden = True
    page.window.full_screen = True
    page.bgcolor = ft.Colors.WHITE
    page.padding = 0
    page.theme = ft.Theme(font_family="MiSans")

    card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "主标题",
                        size=30,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text("这是一个副标题", size=20, color=ft.Colors.GREY_600),
                ]
            ),
            width=800,
            height=600,
            padding=20,
            alignment=ft.alignment.center,
        ),
        elevation=4,
        color=ft.Colors.GREY_200,
    )

    page.add(
        ft.Container(
            content=card,
            alignment=ft.alignment.center,
            expand=True,
        )
    )


ft.app(target=main)
