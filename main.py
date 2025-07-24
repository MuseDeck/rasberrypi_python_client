import flet as ft
from http_client import HTTP_Client
from adptars import DataModel
from gesture_sensor import GestureSensor


def main(page: ft.Page):
    page.title = "Daily Dashboard"
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 40
    page.window.full_screen = True

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

        # Update calendar section
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

        # Update other sections
        recipe_title_control.value = data.recipe.title
        recipe_content_control.value = data.recipe.content
        inspiration_title_control.value = data.inspiration.title
        inspiration_content_control.value = data.inspiration.content
        inspiration_source_control.value = data.inspiration.source
        quote_control.value = data.daily_quote.quote
        author_control.value = data.daily_quote.author
        source_control.value = data.daily_quote.source

        page.update()

    def gesture_sensor_daemon_thread():
        gs = GestureSensor(lambda _: update_data())
        gs.start()

    page.run_task(update_data)
    page.run_thread(gesture_sensor_daemon_thread)

    # Header
    header = ft.Container(
        ft.Text(
            "🌅 Daily Dashboard",
            style="displayMedium",
            weight="bold",
            color=ft.Colors.BLUE_900,
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

    # Calendar Section
    calendar_section = ft.Container(
        calendar_secion_column,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=12, color=ft.Colors.BLUE_100, offset=ft.Offset(0, 4)
        ),
        expand=1,
        margin=ft.margin.only(bottom=10),
    )

    recipe_section = ft.Container(
        ft.Column(
            [
                recipe_title_control,
                recipe_content_control,
                ft.Text("Ingredients:", weight="bold", color=ft.Colors.PINK_700),
                ft.Text("Instructions:", weight="bold", color=ft.Colors.PINK_700),
            ],
            spacing=8,
        ),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=12, color=ft.Colors.PINK_100, offset=ft.Offset(0, 4)
        ),
        expand=1,
        margin=ft.margin.only(bottom=10),
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
        expand=1,
        margin=ft.margin.only(bottom=10),
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
        expand=1,
        margin=ft.margin.only(bottom=10),
    )

    page.add(
        header,
        ft.ResponsiveRow(
            [calendar_section, recipe_section],
            spacing=20,
            run_spacing=20,
        ),
        ft.ResponsiveRow(
            [inspiration_section, daily_quote_section], spacing=20, run_spacing=20
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)
