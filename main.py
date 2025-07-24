from http_client import HTTP_Client
import logging

if __name__ == "__main__":
    try:
        http = HTTP_Client()
        result = http.get()
        print("API JSON Response:", result)
    except Exception as e:
        logging.error(f"Failed to fetch JSON from API: {e}")
