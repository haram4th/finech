import os
import requests
from datetime import datetime, timedelta
import google.generativeai as genai
from fastapi import HTTPException
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.models import News
from app.services.stock_service import get_company_news
from typing import List, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        # 모의 뉴스 데이터
        self.mock_news = {
            'AAPL': [
                {
                    'headline': 'Apple Reports Record Q1 2024 Earnings',
                    'summary': 'Apple Inc. reported record-breaking earnings for Q1 2024, exceeding analyst expectations with strong iPhone and Services revenue.',
                    'source': 'Financial Times',
                    'datetime': (datetime.now() - timedelta(days=1)).isoformat(),
                    'sentiment_score': 0.8
                },
                {
                    'headline': 'Apple Vision Pro Sales Surpass Expectations',
                    'summary': 'The new Apple Vision Pro has seen strong initial sales, with analysts projecting significant growth in the AR/VR market.',
                    'source': 'TechCrunch',
                    'datetime': (datetime.now() - timedelta(days=2)).isoformat(),
                    'sentiment_score': 0.7
                },
                {
                    'headline': 'Apple Expands AI Integration Across Products',
                    'summary': 'Apple announces major AI features coming to iOS and macOS, showcasing commitment to artificial intelligence innovation.',
                    'source': 'Bloomberg',
                    'datetime': (datetime.now() - timedelta(days=3)).isoformat(),
                    'sentiment_score': 0.6
                }
            ],
            'MSFT': [
                {
                    'headline': 'Microsoft AI Revenue Soars in Q1',
                    'summary': 'Microsoft reports significant growth in AI-related revenue, driven by Azure AI and Copilot adoption across enterprise customers.',
                    'source': 'Reuters',
                    'datetime': (datetime.now() - timedelta(days=1)).isoformat(),
                    'sentiment_score': 0.9
                },
                {
                    'headline': 'Microsoft Expands Cloud Infrastructure',
                    'summary': 'Company announces major expansion of data centers globally to meet growing demand for cloud and AI services.',
                    'source': 'Bloomberg',
                    'datetime': (datetime.now() - timedelta(days=2)).isoformat(),
                    'sentiment_score': 0.7
                },
                {
                    'headline': 'Microsoft Teams Gets AI-Powered Features',
                    'summary': 'New AI features in Microsoft Teams aim to improve meeting productivity and collaboration experience.',
                    'source': 'TechCrunch',
                    'datetime': (datetime.now() - timedelta(days=3)).isoformat(),
                    'sentiment_score': 0.8
                }
            ]
        }

    async def get_company_news(self, symbol: str):
        """회사 관련 뉴스를 가져옵니다."""
        try:
            logger.info(f"Fetching news for symbol: {symbol}")
            if not symbol:
                logger.error("Symbol is empty")
                return []
                
            if symbol in self.mock_news:
                logger.info(f"Found mock news for {symbol}")
                return self.mock_news[symbol]
                
            logger.info(f"No mock news found for {symbol}")
            return []
            
        except Exception as e:
            logger.error(f"Error in get_company_news for {symbol}: {str(e)}")
            return []  # 에러 발생 시 빈 리스트 반환

    async def get_news_summary(self, symbol: str):
        """뉴스 내용을 요약합니다."""
        try:
            news_data = await self.get_company_news(symbol)
            if not news_data:
                return {"summary": "No news available"}

            # 뉴스 요약 생성
            summary = "Recent company highlights:\n\n"
            for news in news_data:
                summary += f"- {news['headline']}: {news['summary']}\n"

            return {
                "summary": summary,
                "original_news": news_data
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate news summary: {str(e)}")

async def get_stock_news(symbol: str, db: Session = None) -> List[dict]:
    """주식 관련 뉴스를 가져오고 처리합니다."""
    try:
        news_service = NewsService()
        return await news_service.get_company_news(symbol)
    except Exception as e:
        print(f"Error processing news: {e}")
        return []

async def summarize_text(text: str) -> str:
    """텍스트를 요약합니다."""
    try:
        prompt = f"""
        다음 뉴스 기사를 3-4문장으로 요약해주세요. 
        주요 포인트와 투자자에게 중요한 정보를 중심으로 요약해주세요.
        
        뉴스 내용:
        {text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return text[:200] + "..."  # 에러 발생 시 간단히 자르기

async def analyze_sentiment(text: str) -> float:
    """텍스트의 감성을 분석합니다. (-1: 매우 부정적, 0: 중립, 1: 매우 긍정적)"""
    try:
        prompt = f"""
        다음 뉴스 기사의 투자 관점에서의 감성을 분석해주세요.
        -1(매우 부정적)에서 1(매우 긍정적) 사이의 숫자로 표현해주세요.
        숫자만 반환해주세요.
        
        뉴스 내용:
        {text}
        """
        
        response = model.generate_content(prompt)
        sentiment_score = float(response.text.strip())
        return max(min(sentiment_score, 1.0), -1.0)  # 범위 제한
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0  # 에러 발생 시 중립 반환

async def get_news_summaries(symbol: str, db: Session) -> List[dict]:
    """특정 주식의 뉴스 요약을 가져옵니다."""
    try:
        news_items = db.query(News).filter(News.stock_id == symbol).order_by(News.published_at.desc()).limit(10).all()
        return [
            {
                'title': news.title,
                'summary': news.summary,
                'sentiment_score': news.sentiment_score,
                'source': news.source,
                'published_at': news.published_at.isoformat()
            }
            for news in news_items
        ]
    except Exception as e:
        print(f"Error getting news summaries: {e}")
        return [] 