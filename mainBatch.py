from main import *
import time

if __name__ == "__main__":
    for i in range(10001):
        time.sleep(0.5)
        print(i)
        get_content_from_search(f"Search {i}")
