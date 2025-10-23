from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import requests, os, re
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env_naver")  # 환경변수 로드

app = FastAPI()

def text_clean(text):
    text = re.sub(r"</?[^>]+>", "", text)
    text = re.sub(r"[^가-힣a-zA-Z0-9]", " ", text)
    return " ".join(text.split())

def naver_blog_search(keyword):
    url = "https://openapi.naver.com/v1/search/blog"
    headers = {
        "X-Naver-Client-Id": os.getenv("user_Id"),
        "X-Naver-Client-Secret": os.getenv("user_Secret")
    }
    params = {"query": keyword, "display": 10, "sort": "date"}
    r = requests.get(url, headers=headers, params=params)
    data = r.json()
    return [
        {
            "title": text_clean(i["title"]),
            "desc": text_clean(i["description"]),
            "link": i["link"]
        }
        for i in data.get("items", [])
    ]

@app.get("/", response_class=HTMLResponse)
def form_page():
    return """
    <h2>🔍 네이버 블로그 검색</h2>
    <form action="/search" method="post">
        <input type="text" name="keyword" placeholder="검색어 입력" required>
        <button type="submit">검색</button>
    </form>
    """

@app.post("/search", response_class=HTMLResponse)
def search(keyword: str = Form(...)):
    results = naver_blog_search(keyword)
    html = f"<h3>‘{keyword}’ 검색 결과</h3><ul>"
    for r in results:
        html += f"<li><a href='{r['link']}' target='_blank'>{r['title']}</a><br>{r['desc']}</li><br>"
    html += "</ul><a href='/'>돌아가기</a>"
    return html
