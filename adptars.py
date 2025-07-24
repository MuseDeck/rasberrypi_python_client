from pydantic import ValidationError
from pydantic import BaseModel
from typing import List
from http_client import HTTP_Client
from pprint import pprint

class DailyQuote(BaseModel):
    author: str
    quote: str
    source: str

class Recipe(BaseModel):
    content: str
    keyword: List[str]
    source: str
    title: str

class Event(BaseModel):
    description: str
    time: str

class Calendar(BaseModel):
    title: str
    events: List[Event]

class Inspiration(BaseModel):
    content: str
    keyword: List[str]
    source: str
    title: str

class DataModel(BaseModel):
    daily_quote: DailyQuote
    recipe: Recipe
    calendar: Calendar
    inspiration: Inspiration


if __name__ == "__main__":    
    try:
        http_client = HTTP_Client()
        json_data = http_client.get()
        pprint(json_data)
        data = DataModel(**json_data)
        print(data.daily_quote.author)
        print(data.recipe.title)
        print(data.recipe.content)
        print(data.calendar.title)
        for event in data.calendar.events:
            print(f"- {event.description} at {event.time}")
        print(data.inspiration.content)
    except ValidationError as e:
        print("data valid error:", e)