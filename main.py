import flet as ft
from http_client import HTTP_Client
import logging

def main(page: ft.Page):
    page.title = "Daily Dashboard"
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.padding = 40

    # Header
    header = ft.Container(
        ft.Text("🌅 Daily Dashboard", style="displayMedium", weight="bold", color=ft.colors.BLUE_900),
        alignment=ft.alignment.center,
        padding=20,
        margin=ft.margin.only(bottom=30),
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=18, color=ft.colors.BLUE_GREY_200, offset=ft.Offset(0, 8)),
    )

    try:
        http = HTTP_Client()
        result = http.get()
    except Exception as e:
        logging.error(f"Failed to fetch JSON from API: {e}")
        page.add(header, ft.Text(f"Failed to fetch data: {e}", color="red"))
        return

    # Calendar Section
    calendar = result.get("calendar", {})
    calendar_title = calendar.get("title", "Calendar")
    events = calendar.get("events", [])
    calendar_section = ft.Container(
        ft.Column([
            ft.Text(calendar_title, style="titleLarge", weight="bold", color=ft.colors.BLUE_700),
            *(ft.Text(f"{event['time']} — {event['description']}", size=16, color=ft.colors.BLUE_GREY_900) for event in events)
        ], spacing=8),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLUE_100, offset=ft.Offset(0, 4)),
        expand=1,
        margin=ft.margin.only(right=10)
    )

    # Recipe Section
    recipe = result.get("recipe", {})
    recipe_title = recipe.get("title", "Recipe")
    recipe_name = recipe.get("name", "")
    ingredients = recipe.get("ingredients", [])
    instructions = recipe.get("instructions", "")
    recipe_section = ft.Container(
        ft.Column([
            ft.Text(recipe_title, style="titleLarge", weight="bold", color=ft.colors.PINK_700),
            ft.Text(f"🍳 {recipe_name}", weight="bold", size=18, color=ft.colors.PINK_900),
            ft.Text("Ingredients:", weight="bold", color=ft.colors.PINK_700),
            *(ft.Text(f"- {ing}", color=ft.colors.PINK_800) for ing in ingredients),
            ft.Text("Instructions:", weight="bold", color=ft.colors.PINK_700),
            ft.Text(instructions, color=ft.colors.PINK_900)
        ], spacing=8),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.PINK_100, offset=ft.Offset(0, 4)),
        expand=1,
        margin=ft.margin.only(left=10)
    )

    # Inspiration Section
    inspiration = result.get("inspiration", {})
    inspiration_title = inspiration.get("title", "Inspiration")
    inspiration_content = inspiration.get("content", "")
    inspiration_source = inspiration.get("source", "")
    inspiration_section = ft.Container(
        ft.Column([
            ft.Text(inspiration_title, style="titleLarge", weight="bold", color=ft.colors.TEAL_700),
            ft.Text(f"“{inspiration_content}”", italic=True, size=16, color=ft.colors.TEAL_900),
            ft.Text(f"Source: {inspiration_source}", size=12, color=ft.colors.TEAL_400)
        ], spacing=8),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.TEAL_100, offset=ft.Offset(0, 4)),
        expand=1,
        margin=ft.margin.only(right=10)
    )

    # Daily Quote Section
    daily_quote = result.get("daily_quote", {})
    quote = daily_quote.get("quote", "")
    author = daily_quote.get("author", "")
    source = daily_quote.get("source", "")
    daily_quote_section = ft.Container(
        ft.Column([
            ft.Text("Daily Quote", style="titleLarge", weight="bold", color=ft.colors.AMBER_800),
            ft.Text(f'“{quote}”', italic=True, size=16, color=ft.colors.AMBER_900),
            ft.Text(f"- {author}", size=14, color=ft.colors.AMBER_700),
            ft.Text(f"Source: {source}", size=12, color=ft.colors.AMBER_400)
        ], spacing=8),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.AMBER_100, offset=ft.Offset(0, 4)),
        expand=1,
        margin=ft.margin.only(left=10)
    )

    # Layout
    page.add(
        header,
        ft.ResponsiveRow([
            calendar_section,
            recipe_section
        ], spacing=20, run_spacing=20),
        ft.ResponsiveRow([
            inspiration_section,
            daily_quote_section
        ], spacing=20, run_spacing=20)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
