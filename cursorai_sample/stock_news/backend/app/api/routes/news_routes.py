from fastapi import APIRouter, HTTPException
from app.services.news_service import NewsService
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
news_service = NewsService()

class NewsItem(BaseModel):
    id: int
    title: str
    content: str
    summary: str
    published_at: datetime
    sentiment_score: float
    source: str

@router.get("/{symbol}", response_model=List[NewsItem])
async def get_stock_news(symbol: str):
    try:
        return await news_service.get_stock_news(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/sentiment")
async def get_news_sentiment(symbol: str):
    try:
        return await news_service.get_news_sentiment(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 