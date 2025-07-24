import requests
import os
import logging
import aiohttp
from pprint import pformat

logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv

load_dotenv()

GET_API_URL = os.getenv("GET_API_URL")
assert GET_API_URL is not None


class HTTP_Client:
    def __init__(self):
        pass

    def get(self):
        return requests.get(GET_API_URL).json()
    
    async def get_async(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(GET_API_URL) as response:
                return await response.json()


if __name__ == "__main__":
    # simple test
    http = HTTP_Client()
    logging.info(pformat(http.get()))
