from pydantic import ValidationError
from pydantic import BaseModel
from typing import List

class DailyQuote(BaseModel):
    author: str
    quote: str
    source: str

class Recipe(BaseModel):
    name: str
    title: str
    ingredients: List[str]
    instructions: str

class DataModel(BaseModel):
    daily_quote: DailyQuote
    recipe: Recipe


if __name__ == "__main__":
    # simple test
    json_data = {
        "daily_quote": {
            "author": "@路人威",
            "quote": "眼泪无法洗去痛苦，但岁月可以抹去一切。",
            "source": "网易云音乐",
        },
        "recipe": {
            "ingredients": ["Tomatoes", "Eggs", "Scallions", "Salt"],
            "instructions": "1. Scramble eggs 2. Stir-fry tomatoes 3. Combine",
            "name": "Stir-fried Tomatoes with Eggs",
            "title": "Today's Recommended Recipe",
        },
    }
    try:
        data = DataModel(**json_data)
        print(data.daily_quote.author)
        print(data.recipe.name)
        print(data.recipe.ingredients)
    except ValidationError as e:
        print("data valid error:", e)
