import json
import sys
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

def get_content_from_search(search_term):
    r = google_search(search_term)
    results = r["items"][:MAX_AMOUNT]
    for result in results:
        page_text = get_page_text(result['link'])
        return (result['title'], result['link'], page_text)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong amount of parameters passed, usage: main.py <search-term>")
    else:
        contentTuple = get_content_from_search(sys.argv[1])
        print(contentTuple)
    
