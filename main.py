import flet as ft
import logging
from http_client import HTTP_Client
from mqtt_client import MQTT_Client
from adptars import DataModel
from time import sleep
from typing import List
from adptars import DailyQuote
from db import DB
from camera import predict_face
import cv2

OVERVIEW_ROUTE = "/overview"
FAVORITES_ROUTE = "/favorites"


def main(page: ft.Page):
    page.title = "Muse Deck"
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 10
    page.window.full_screen = True
    page.theme = ft.Theme(font_family="Droid Sans Fallback")

    def quote_card(quote: DailyQuote):
        return ft.Card(
            content=ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            quote.quote,
                            italic=True,
                            size=16,
                            color=ft.Colors.AMBER_900,
                        ),
                        ft.Text(
                            f"- {quote.author}",
                            size=14,
                            color=ft.Colors.AMBER_700,
                        ),
                        ft.Text(
                            f"Source: {quote.source}",
                            size=12,
                            color=ft.Colors.AMBER_400,
                        ),
                    ],
                    spacing=8,
                ),
                padding=20,
            ),
            expand=True,
        )

    def route_change(e):
        page.views.clear()
        title_control.value = "Muse Deck"
        if page.route == OVERVIEW_ROUTE:
            logging.info("overview route")
            page.views.append(
                ft.View(
                    OVERVIEW_ROUTE,
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
            page.run_thread(update_data)
            page.run_thread(gesture_sensor_daemon_thread, page)
            page.run_thread(face_detection_daemon_thread)

        if page.route == FAVORITES_ROUTE:
            logging.info("favorites route")
            quotes = db.get_all_daily_quote_to_favorite()
            page.views.append(
                ft.View(
                    FAVORITES_ROUTE,
                    controls=[
                        header,
                        ft.Row(
                            [quote_card(quote) for quote in quotes],
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

    async def popover_insprition_card():
        model = DataModel(**(await http_client.get_async()))
        inspiration_banner_column.controls = [
            ft.Text(
                model.inspiration.title,
                size=20,
                color=ft.Colors.BLUE_GREY_900,
            ),
            ft.Text(
                model.inspiration.content,
                size=20,
                color=ft.Colors.BLUE_GREY_900,
            ),
            ft.Text(
                model.inspiration.source,
                size=20,
                color=ft.Colors.BLUE_GREY_900,
            ),
        ]
        if not detected_flag:
            page.update()
            page.open(banner)

    quote_control = ft.Text(f"quote", italic=True, size=16, color=ft.Colors.AMBER_900)
    author_control = ft.Text(f"- author", size=14, color=ft.Colors.AMBER_700)
    source_control = ft.Text(f"Source: source", size=12, color=ft.Colors.AMBER_400)
    http_client = HTTP_Client()

    mqtt_client = MQTT_Client(
        inspiration_action=lambda: page.run_task(popover_insprition_card),
        settings_action=lambda: page.run_thraed(update_data),
    )
    page.run_thread(mqtt_client.run)

    # def camera_thread(callback):
    #     cap = cv2.VideoCapture(0)
    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         result = predict_face(frame)
    #         if result.face_count == 0:
    #             continue
    #         max_face = max(result.faces, key=lambda x: x.w * x.h)
    #         if max_face.w * max_face.h > 10000:
    #             callback()
    
    def update_data():
        result = http_client.get()
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

    db = DB()

    def on_gesture_changed(gesture_name):
        nonlocal detected_flag
        global OVERVIEW_ROUTE, FAVORITES_ROUTE
        if banner.open:
            page.close(banner)
            detected_flag = False
            return
        logging.info(f"Gesture: {gesture_name}")

        if gesture_name == "Left":
            if page.route == FAVORITES_ROUTE:
                page.go(OVERVIEW_ROUTE)
            else:
                page.go(FAVORITES_ROUTE)
        elif gesture_name == "Right":
            if page.route == OVERVIEW_ROUTE:
                page.go(FAVORITES_ROUTE)
            else:
                page.go(OVERVIEW_ROUTE)
        else:
            if page.route == OVERVIEW_ROUTE:
                match gesture_name:
                    case "Forward":
                        logging.info("🤡收藏")
                        quote = DailyQuote(
                            quote=quote_control.value,
                            author=author_control.value,
                            source=source_control.value,
                        )
                        db.add_daily_quote_to_favorite(quote)
                        page.open(ft.SnackBar(ft.Text("收藏成功")))
                        page.update()

    def gesture_sensor_daemon_thread(page):
        logging.info("gesture_sensor init")
        import platform

        if platform.system() != "Linux":
            return
        logging.info("gesture_sensor start")
        from gesture_sensor import GestureSensor

        gs = GestureSensor(lambda x: on_gesture_changed(x))
        gs.start()

    detected_flag = False

    def face_detection_daemon_thread():
        nonlocal detected_flag
        cap = cv2.VideoCapture(0)
        i = 0
        while True:
            if not banner.open:
                detected_flag = False
                i = 0
                continue
            i += 1
            if (i > 6 and not detected_flag):
                i = 0
                page.close(banner)
            if cap.isOpened() and banner.open:
                ret, frame = cap.read()
                result = predict_face(frame)
                if result.face_count == 0:
                    # continue
                    logging.info("Face not detected")
                    logging.info(i)
                    logging.info(detected_flag)
                else:
                    max_face = max(result.faces, key=lambda x: x.w * x.h)
                    if max_face.w * max_face.h > 25000:
                        detected_flag = True
                        i = 0
                        logging.info("Face detected!!!⚠️")
                    else:
                        logging.info("Face not detected")
                        logging.info(i)
                        logging.info(detected_flag)
                sleep(0.5)

        # while cap.isOpened():
        #     ret, frame = cap.read()
        #     result = predict_face(frame)
        #     if result.face_count == 0:
        #         continue
        #     max_face = max(result.faces, key=lambda x: x.w * x.h)
        #     if max_face.w * max_face.h > 10000:
        #         detected_flag = True
        #     sleep(0.1)
        
        # while True:
        #     if not banner.open:
        #         continue
        #     result = predict_face()
        #     if result.face_count > 0:
        #         max_face = max(result.faces, key=lambda x: x.w * x.h)
        #         max_face_area = max_face.w * max_face.h
        #         logging.info
        #         if max_face_area > FACE_AREA:
        #             logging.info("Detected face")
        #             detected_flag = True
        #         else:
        #             logging.info("No Detecting face")
        #             if banner.open and (not detected_flag):
        #                 page.close(banner)
        #                 detected_flag = False
        #     else:
        #         logging.info("No Detecting face")
        #         if banner.open:
        #             page.close(banner)

    logo_img = ft.Image(
        src="logo.png",
        width=60,
        height=60,
        fit=ft.ImageFit.CONTAIN,
    )

    header = ft.Container(
        ft.Row(
            [
                logo_img,
                title_control := ft.Text(
                    "Muse Deck",
                    style="displayMedium",
                    weight="bold",
                    color=ft.Colors.BLUE_900,
                    size=32,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        padding=5,
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

    page.overlay.append(banner)

    page.on_route_change = route_change
    page.go(OVERVIEW_ROUTE)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
