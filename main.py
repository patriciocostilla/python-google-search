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
    try:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, features="html.parser")
        page_text = soup.body.get_text()
        return page_text.strip()
    except:
        return "Scraping error"

def get_content_from_search(search_term):
    r = google_search(search_term)
    search_results = r["items"]
    scraped_content = []
    for result in search_results:
        page_text = get_page_text(result['link'])
        scraped_content.append({'title': result['title'], 'link': result['link'], 'page_text': page_text})
        if len(scraped_content) >= MAX_AMOUNT:
            break
    return scraped_content

def get_content_only(search_term):
    scraped_content = get_content_from_search(search_term)
    content = ""
    for item in scraped_content:
        content = content + "\n" + item['page_text']
    return content


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong amount of parameters passed, usage: main.py <search-term>")
    else:
        # scraped_content = get_content_from_search(sys.argv[1])
        # print(scraped_content)
        content = get_content_only(sys.argv[1])
        print(content)
    
