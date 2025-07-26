from pydantic import ValidationError
from pydantic import BaseModel
from typing import List, Optional
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
    daily_quote: Optional[DailyQuote] = None
    recipe: Optional[Recipe] = None
    calendar: Optional[Calendar] = None
    inspiration: Optional[Inspiration] = None


class Face(BaseModel):
    x: int
    y: int
    w: int
    h: int


class FaceDetectionResult(BaseModel):
    face_count: int
    faces: List[Face]


if __name__ == "__main__":
    try:
        http_client = HTTP_Client()
        json_data = http_client.get()
        pprint(json_data)
        data = DataModel(**json_data)
        print(data.daily_quote.author if data.daily_quote else "No Quote")
        print(data.recipe.title if data.recipe else "No Recipe")
        print(data.recipe.content if data.recipe else "No Recipe Content")
        print(data.calendar.title if data.calendar else "No Calendar")
        for event in data.calendar.events if data.calendar else []:
            print(f"- {event.description} at {event.time}")
        print(data.inspiration.content if data.inspiration else "No Inspiration")
    except ValidationError as e:
        print("data valid error:", e)
