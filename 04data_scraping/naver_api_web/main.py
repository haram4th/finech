# main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from naver_api import naver_blog_search

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request):  # ← 여기만 타입힌트 필요
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
def search(request: Request, keyword=Form(...)):  # ← 여기도 Request만 타입힌트
    results = naver_blog_search(keyword)
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "keyword": keyword, "results": results}
    )
