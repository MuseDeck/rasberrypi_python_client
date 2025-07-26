from pathlib import Path
from adptars import DailyQuote
from pickle import dump, load
from typing import List
from pprint import pp


class DB:
    def __init__(self):
        self.daily_quote_db_path = Path("./daiky_quote.pkl")

    def add_daily_quote_to_favorite(self, daily_quote: DailyQuote):
        if not self.daily_quote_db_path.exists():
            with open(self.daily_quote_db_path, "wb") as f:
                dump([], f)
        
        with open(self.daily_quote_db_path, "rb") as f:
            try:
                daily_quote_list: List[DailyQuote] = load(f)
            except EOFError:
                daily_quote_list = []
            daily_quote_list.append(daily_quote)
        with open(self.daily_quote_db_path, "wb") as f:
            dump(daily_quote_list, f)
    
    def clear_daily_quote(self):
        with open(self.daily_quote_db_path, "wb") as f:
            dump([],f)
        
    def get_all_daily_quote_to_favorite(self):
        if not self.daily_quote_db_path.exists():
            return []
        try:
            with open(self.daily_quote_db_path,"rb") as f:
                daily_quote_list: List[DailyQuote] = load(f)
            return daily_quote_list
        except EOFError:
            return []


if __name__ == "__main__":
    db = DB()
    q = db.get_all_daily_quote_to_favorite()
    pp(q)
    for i in range(2):
        db.add_daily_quote_to_favorite(
            DailyQuote(
                author="author",
                quote="quote",
                source="source"
            )
        )
    q = db.get_all_daily_quote_to_favorite()
    pp(q)
    db.clear_daily_quote()
    q = db.get_all_daily_quote_to_favorite()
    pp(q)