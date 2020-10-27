import json
from googleapiclient.discovery import build
from constants import *
import requests
from bs4 import BeautifulSoup

def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=search_term, cx=CSE_ID, **kwargs).execute()
    return res

def get_page_text(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    page_text = soup.body.get_text()
    return page_text.strip()


if __name__ == "__main__":
    r = google_search("Hello world!")
    results = r["items"][:MAX_AMOUNT]
    print(results[0])
    for result in results:
        print(f"{result['title']}: {result['link']}")
        page_text = get_page_text(result['link'])
        print(f"page text: {page_text}")