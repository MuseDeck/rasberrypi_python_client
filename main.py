import flet as ft
from http_client import HTTP_Client
from adptars import DataModel
from camera import Camera
from time import sleep


def main(page: ft.Page):
    page.title = "Muse Deck"
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 10
    page.window.full_screen = True
    page.theme = ft.Theme(font_family="Droid Sans Fallback")

    def route_change(e):
        page.views.clear()
        if page.route == "/overview" or page.route == "/":
            page.views.append(
                ft.View(
                    "/overview",
                    controls=[
                        header,
                        ft.Row(
                            [calendar_section, recipe_section, daily_quote_section],
                            spacing=20,
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                    ],
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    padding=10,
                    scroll=ft.ScrollMode.AUTO,
                )
            )
        page.update()

    calendar_title_control = ft.Text(
        "Calendar Title",
        style="titleLarge",
        weight="bold",
        color=ft.Colors.BLUE_700,
    )
    calendar_secion_column = ft.Column(
        [
            calendar_title_control,
        ],
        spacing=8,
    )

    recipe_title_control = ft.Text(
        "recipe_title",
        style="titleLarge",
        weight="bold",
        color=ft.Colors.PINK_700,
    )
    recipe_content_control = ft.Text(
        f"recipe_name",
        weight="bold",
        size=18,
        color=ft.Colors.PINK_900,
    )

    quote_control = ft.Text(f"quote", italic=True, size=16, color=ft.Colors.AMBER_900)
    author_control = ft.Text(f"- author", size=14, color=ft.Colors.AMBER_700)
    source_control = ft.Text(f"Source: source", size=12, color=ft.Colors.AMBER_400)
    http_client = HTTP_Client()

    async def update_data():
        result = await http_client.get_async()
        data = DataModel(**result)

        if data.calendar:
            calendar_title_control.value = data.calendar.title
            calendar_secion_column.controls.clear()
            calendar_secion_column.controls.append(calendar_title_control)
            for event in data.calendar.events:
                calendar_secion_column.controls.append(
                    ft.Text(
                        f"{event.time} — {event.description}",
                        size=16,
                        color=ft.Colors.BLUE_GREY_900,
                    )
                )

        if data.recipe:
            recipe_title_control.value = data.recipe.title
            recipe_content_control.value = data.recipe.content
            recipe_section.visible = True
        else:
            recipe_section.visible = False

        if data.daily_quote:
            quote_control.value = data.daily_quote.quote
            author_control.value = data.daily_quote.author
            source_control.value = data.daily_quote.source
        else:
            quote_control.visible = False

        page.update()

    def launch_update_data(_):
        page.close(banner)
        page.run_task(update_data)
        
    def gesture_sensor_daemon_thread():
        import platform
        if platform.system() != "Linux":
            return
        print("gesture_sensor")
        from gesture_sensor import GestureSensor
        gs = GestureSensor(launch_update_data)
        gs.start()

    def face_detection_daemon_thread():
        camera = Camera()
        FACE_AREA = 100000
        while True:
            result = camera.predict_face(camera.capture_image())
            if result.face_count > 0:
                max_face = max(result.faces, key=lambda x: x.w * x.h)
                max_face_area = max_face.w * max_face.h
                if max_face_area > FACE_AREA:
                    model = DataModel(**http_client.get())
                    inspiration_banner_column.controls = [
                        ft.Text(model.inspiration.title, size=20),
                        ft.Text(model.inspiration.content, size=20),
                        ft.Text(model.inspiration.source, size=20),
                    ]
                    page.open(banner)

            sleep(0.1)

    page.run_task(update_data)
    page.run_thread(gesture_sensor_daemon_thread)
    page.run_thread(face_detection_daemon_thread)

    logo_img = ft.Image(
        src="logo.png",
        width=120,
        height=120,
        fit=ft.ImageFit.CONTAIN,
    )

    header = ft.Container(
        ft.Row(
            [
                ft.Text(
                    "Muse Deck",
                    style="displayMedium",
                    weight="bold",
                    color=ft.Colors.BLUE_900,
                ),
                logo_img,
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=20,
        margin=ft.margin.only(bottom=10),
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(
            blur_radius=18, color=ft.Colors.BLUE_GREY_200, offset=ft.Offset(0, 8)
        ),
    )

    CARD_HEIGHT = 300

    calendar_section = ft.Container(
        calendar_secion_column,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=12, color=ft.Colors.BLUE_100, offset=ft.Offset(0, 4)
        ),
        expand=True,
        margin=ft.margin.only(bottom=10),
        height=CARD_HEIGHT,
    )

    recipe_section = ft.Container(
        ft.Column(
            [
                recipe_title_control,
                recipe_content_control,
            ],
            spacing=8,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=12, color=ft.Colors.PINK_100, offset=ft.Offset(0, 4)
        ),
        expand=True,
        margin=ft.margin.only(bottom=10),
        height=CARD_HEIGHT,
    )

    daily_quote_section = ft.Container(
        ft.Column(
            [
                ft.Text(
                    "Daily Quote",
                    style="titleLarge",
                    weight="bold",
                    color=ft.Colors.AMBER_800,
                ),
                quote_control,
                author_control,
                source_control,
            ],
            spacing=8,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=12, color=ft.Colors.AMBER_100, offset=ft.Offset(0, 4)
        ),
        expand=True,
        margin=ft.margin.only(bottom=10),
        height=CARD_HEIGHT,
    )

    banner = ft.Banner(
        bgcolor=ft.Colors.CYAN_500,
        leading=ft.Icon(ft.Icons.BUBBLE_CHART, color=ft.Colors.WHITE70, size=40),
        content=(
            inspiration_banner_column := ft.Column(
                controls=[],
                spacing=10,
            )
        ),
        actions=[
            ft.TextButton(text="Retry", on_click=lambda _: page.update()),
        ],
    )

    page.on_route_change = route_change
    page.go("/overview")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", port=9000)