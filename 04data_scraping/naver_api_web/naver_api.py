import os, re, requests
from dotenv import load_dotenv

load_dotenv("./data/.env_naver")

def text_clean(text):
    text = re.sub(r"</?[^>]+>", "", text)
    text = re.sub(r"[^가-힣a-zA-Z0-9]", " ", text)
    return " ".join(text.split())

def naver_blog_search(keyword):
    url = "https://openapi.naver.com/v1/search/news"
    headers = {
        "X-Naver-Client-Id": os.getenv("user_Id"),
        "X-Naver-Client-Secret": os.getenv("user_Secret")
    }
    params = {"query": keyword, "display": 50, "sort": "date"}

    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    results = []

    for i in data.get("items", []):
        results.append({
            "title": text_clean(i.get("title", "")),
            "desc": text_clean(i.get("description", "")),
            "link": i.get("link", "")
        })
    return results
