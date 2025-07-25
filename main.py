import flet as ft
from http_client import HTTP_Client
from adptars import DataModel
from camera import Camera


def main(page: ft.Page):
    page.title = "Muse Deck"
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 10
    page.window.full_screen = True
    page.theme = ft.Theme(font_family="Droid Sans Fallback")

    # Initialize controls first
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
        f"🍳 recipe_name",
        weight="bold",
        size=18,
        color=ft.Colors.PINK_900,
    )

    inspiration_title_control = ft.Text(
        "inspiration_title",
        style="titleLarge",
        weight="bold",
        color=ft.Colors.TEAL_700,
    )
    inspiration_content_control = ft.Text(
        f"“inspiration_content”",
        italic=True,
        size=16,
        color=ft.Colors.TEAL_900,
    )
    inspiration_source_control = ft.Text(
        f"Source: inspiration_source", size=12, color=ft.Colors.TEAL_400
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

        if data.inspiration:
            inspiration_title_control.value = data.inspiration.title
            inspiration_content_control.value = data.inspiration.content
            inspiration_source_control.value = data.inspiration.source

        if data.daily_quote:
            quote_control.value = data.daily_quote.quote
            author_control.value = data.daily_quote.author
            source_control.value = data.daily_quote.source

        page.update()
    
    def launch_update_data(_):
        page.run_task(update_data)
        print("data updated")

    def gesture_sensor_daemon_thread():
        import platform
        if platform.system() != "Linux":
            return
        print("gesture_sensor")
        from gesture_sensor import GestureSensor
        gs = GestureSensor(launch_update_data)
        gs.start()

    def people_detection_daemon_thread():
        camera = Camera()
        while True:
            image = camera.picam2.capture_image()
            result = camera.predict_face(image)
            print(result)

    page.run_task(update_data)
    page.run_thread(gesture_sensor_daemon_thread)
    page.run_thread(people_detection_daemon_thread)

    # Add logo image at the top
    logo_img = ft.Image(
        src="logo.png",
        width=120,
        height=120,
        fit=ft.ImageFit.CONTAIN,
    )

    # Header with title and logo (logo on the right, closer to text)
    header = ft.Container(
        ft.Row([
            ft.Text(
                "Muse Deck",
                style="displayMedium",
                weight="bold",
                color=ft.Colors.BLUE_900,
            ),
            logo_img,
        ], spacing=8, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
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

    # Calendar Section
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

    inspiration_section = ft.Container(
        ft.Column(
            [
                inspiration_title_control,
                inspiration_content_control,
                inspiration_source_control,
            ],
            spacing=8,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=12, color=ft.Colors.TEAL_100, offset=ft.Offset(0, 4)
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

    page.add(
        header,
        ft.Row(
            [
                calendar_section,
                recipe_section,
                inspiration_section,
                daily_quote_section,
            ],
            spacing=20,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
        ),
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
