from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services import news_service
from app.schemas.news import NewsResponse, NewsSummaryResponse

router = APIRouter()

@router.get("/{symbol}", response_model=List[NewsResponse])
async def get_stock_news(symbol: str, db: Session = Depends(get_db)):
    """특정 주식 심볼에 대한 최신 뉴스를 가져옵니다."""
    try:
        news = await news_service.get_stock_news(symbol, db)
        return news
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{symbol}/summary", response_model=List[NewsSummaryResponse])
async def get_news_summary(symbol: str, db: Session = Depends(get_db)):
    """특정 주식의 뉴스 요약을 가져옵니다."""
    try:
        summaries = await news_service.get_news_summaries(symbol, db)
        return summaries
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{symbol}/sentiment", response_model=float)
async def get_news_sentiment(symbol: str, db: Session = Depends(get_db)):
    """특정 주식의 뉴스 감성 분석 점수를 가져옵니다."""
    try:
        sentiment = await news_service.get_news_sentiment(symbol, db)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 