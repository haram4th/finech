import os
import requests
from fastapi import HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import Stock
from typing import List, Optional
import yfinance as yf
import finnhub
from app.core.config import settings
import time

class StockService:
    def __init__(self):
        # 테스트용 주식 데이터
        self.mock_stocks = {
            'AAPL': {'name': 'Apple Inc.', 'price': 180.5},
            'MSFT': {'name': 'Microsoft Corporation', 'price': 350.2},
            'GOOGL': {'name': 'Alphabet Inc.', 'price': 140.8},
            'AMZN': {'name': 'Amazon.com Inc.', 'price': 145.2},
            'META': {'name': 'Meta Platforms Inc.', 'price': 480.3}
        }

    async def search_stocks(self, query: str) -> List[dict]:
        try:
            query = query.upper()
            matches = []
            
            for symbol, data in self.mock_stocks.items():
                if query in symbol or query.lower() in data['name'].lower():
                    matches.append({
                        "symbol": symbol,
                        "company_name": data['name'],
                        "current_price": data['price']
                    })
            
            return matches
        except Exception as e:
            raise Exception(f"Failed to search stocks: {str(e)}")

    async def get_stock_info(self, symbol: str) -> dict:
        try:
            symbol = symbol.upper()
            if symbol not in self.mock_stocks:
                raise Exception("Stock not found")
            
            stock = self.mock_stocks[symbol]
            return {
                "symbol": symbol,
                "company_name": stock['name'],
                "current_price": stock['price'],
                "change_percent": 1.5,  # Mock data
                "market_cap": 2500000000000.0,  # Mock data
                "volume": 50000000,  # Mock data
                "pe_ratio": 28.5,  # Mock data
                "dividend_yield": 0.5  # Mock data
            }
        except Exception as e:
            raise Exception(f"Failed to get stock info: {str(e)}")

    async def get_stock_price(self, symbol: str) -> dict:
        try:
            symbol = symbol.upper()
            if symbol not in self.mock_stocks:
                raise Exception("Stock not found")
            
            return {
                "symbol": symbol,
                "price": self.mock_stocks[symbol]['price']
            }
        except Exception as e:
            raise Exception(f"Failed to get stock price: {str(e)}")

    async def get_stock_candles(self, symbol: str, resolution: str = "D", from_time: int = None, to_time: int = None):
        """주식 차트 데이터를 가져옵니다."""
        url = f"{self.base_url}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_time,
            "to": to_time,
            "token": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch stock candles: {str(e)}")

async def get_company_news(symbol: str, days: int = 7) -> List[dict]:
    """회사 관련 뉴스를 가져옵니다."""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        news = finnhub_client.company_news(
            symbol,
            _from=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d')
        )
        
        return [
            {
                'headline': item['headline'],
                'summary': item['summary'],
                'source': item['source'],
                'url': item['url'],
                'datetime': datetime.fromtimestamp(item['datetime']).isoformat()
            }
            for item in news
        ]
    except Exception as e:
        print(f"Error fetching company news: {e}")
        return []

async def get_stock_data(symbol: str, db: Session) -> Optional[Stock]:
    """주식 정보를 데이터베이스에서 가져오거나 업데이트합니다."""
    try:
        # DB에서 주식 정보 조회
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()
        
        # 현재 가격 가져오기
        current_price = await get_stock_price(symbol)
        
        if stock:
            # 기존 주식 정보 업데이트
            stock.current_price = current_price
            stock.last_updated = datetime.utcnow()
        else:
            # 회사 정보 가져오기
            company_profile = await get_stock_info(symbol)
            
            # 새 주식 정보 생성
            stock = Stock(
                symbol=symbol,
                company_name=company_profile.get('name', ''),
                current_price=current_price,
                last_updated=datetime.utcnow()
            )
            db.add(stock)
            
        db.commit()
        return stock
        
    except Exception as e:
        print(f"Error getting stock data: {e}")
        db.rollback()
        return None 