import os
import numpy as np
from datetime import datetime, timedelta
import google.generativeai as genai
from fastapi import HTTPException
from .stock_service import StockService
from .news_service import NewsService
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import yfinance as yf
from typing import List
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class PredictionService:
    def __init__(self):
        self.stock_service = StockService()
        self.news_service = NewsService()
        self.google_ai_key = os.getenv("GOOGLE_AI_KEY")
        
        if not self.google_ai_key:
            raise ValueError("GOOGLE_AI_KEY environment variable is not set")
            
        # Google AI 설정
        genai.configure(api_key=self.google_ai_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # 데이터 스케일링을 위한 scaler 초기화
        self.scaler = MinMaxScaler()

        self.model = LinearRegression()
        self.last_accuracy = {}  # 심볼별 마지막 정확도 저장

        # 모의 예측 데이터
        self.mock_predictions = {
            'AAPL': {
                'current_price': 180.5,
                'ma5': 178.2,
                'ma20': 175.8,
                'rsi': 65.4,
                'sentiment': 'positive',
                'prediction_summary': '최근 실적 호조와 Vision Pro 출시로 인한 긍정적 전망',
                'predictions': self._generate_predictions(180.5)
            },
            'MSFT': {
                'current_price': 420.5,
                'ma5': 418.2,
                'ma20': 415.8,
                'rsi': 72.4,
                'sentiment': 'very positive',
                'prediction_summary': 'AI 사업 성장과 클라우드 시장 점유율 확대로 매우 긍정적 전망',
                'predictions': self._generate_predictions(420.5)
            }
        }

    def _generate_predictions(self, base_price: float):
        """주가 예측 데이터를 생성합니다."""
        dates = []
        actual_prices = []
        predicted_prices = []
        confidence_scores = []
        
        # 과거 5일 데이터
        for i in range(5, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            price = base_price * (1 + np.random.normal(0, 0.01))
            dates.append(date)
            actual_prices.append(round(price, 2))
            predicted_prices.append(None)
            confidence_scores.append(None)
        
        # 현재 및 미래 10일 예측
        for i in range(11):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            price = base_price * (1 + np.random.normal(0.001 * i, 0.02))
            confidence = max(0.9 - (i * 0.05), 0.5)  # 시간이 지날수록 신뢰도 감소
            dates.append(date)
            actual_prices.append(None)
            predicted_prices.append(round(price, 2))
            confidence_scores.append(round(confidence, 2))
        
        return [
            {
                'date': date,
                'actual_price': actual,
                'predicted_price': predicted,
                'confidence_score': confidence
            }
            for date, actual, predicted, confidence in zip(dates, actual_prices, predicted_prices, confidence_scores)
        ]

    async def get_stock_prediction(self, symbol: str):
        """주가 예측을 수행합니다."""
        try:
            if symbol in self.mock_predictions:
                return self.mock_predictions[symbol]
            return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate prediction: {str(e)}")

    async def get_news_sentiment(self, symbol: str):
        """뉴스 감성 분석을 수행합니다."""
        try:
            # 뉴스 데이터 가져오기
            news_data = await self.news_service.get_company_news(symbol)
            if not news_data:
                return {
                    "sentiment": "neutral",
                    "explanation": "No recent news available for sentiment analysis"
                }

            # 최근 5개 뉴스 제목과 내용 추출
            news_texts = []
            for news in news_data[:5]:
                news_texts.append(f"Title: {news['headline']}\nSummary: {news['summary']}")
            
            # 뉴스 텍스트 결합
            combined_news = "\n\n".join(news_texts)
            
            # Google AI를 사용하여 감성 분석
            prompt = f"""
            다음 뉴스들의 전반적인 감성(긍정/부정/중립)을 분석하고, 주가에 미칠 영향을 설명해주세요.
            분석 결과는 다음 형식으로 작성해주세요:
            - 감성: [긍정/부정/중립]
            - 설명: [주가에 미칠 영향에 대한 설명]

            뉴스:
            {combined_news}
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # 응답 파싱
            sentiment = "neutral"
            if "긍정" in response_text:
                sentiment = "positive"
            elif "부정" in response_text:
                sentiment = "negative"
            
            return {
                "sentiment": sentiment,
                "explanation": response_text
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to analyze news sentiment: {str(e)}")

    def calculate_rsi(self, prices, periods=14):
        """RSI(Relative Strength Index) 계산"""
        deltas = np.diff(prices)
        seed = deltas[:periods+1]
        up = seed[seed >= 0].sum()/periods
        down = -seed[seed < 0].sum()/periods
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:periods] = 100. - 100./(1. + rs)

        for i in range(periods, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(periods-1) + upval)/periods
            down = (down*(periods-1) + downval)/periods
            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)

        return rsi 

    async def get_price_predictions(self, symbol: str) -> List[dict]:
        """향후 10일간의 주가 예측을 생성합니다."""
        try:
            base_price = 180.5  # AAPL 기준가
            if symbol == 'AAPL':
                predictions = []
                current_date = datetime.now()
                
                # 과거 5일 데이터
                for i in range(5):
                    date = current_date - timedelta(days=5-i)
                    predictions.append({
                        "date": date.date(),
                        "actual_price": base_price - 2 + (i * 0.5),
                        "predicted_price": base_price - 2 + (i * 0.5),
                        "confidence_score": 1.0
                    })
                
                # 향후 10일 예측
                for i in range(10):
                    date = current_date + timedelta(days=i+1)
                    # 약간의 랜덤성을 추가한 예측 가격
                    random_change = np.random.normal(0, 1)
                    pred_price = base_price + (i * 0.3) + random_change
                    
                    predictions.append({
                        "date": date.date(),
                        "actual_price": None,
                        "predicted_price": float(pred_price),
                        "confidence_score": max(0.2, 0.9 - (i * 0.05))  # 시간이 지날수록 신뢰도 감소
                    })
                
                return predictions
            else:
                return []
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate predictions: {str(e)}")

    async def get_prediction_accuracy(self, symbol: str) -> float:
        """예측 정확도를 반환합니다."""
        try:
            return 0.85 if symbol == 'AAPL' else 0.0
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get prediction accuracy: {str(e)}") 