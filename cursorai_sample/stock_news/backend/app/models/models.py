from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True)
    company_name = Column(String(100))
    current_price = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    news = relationship("News", back_populates="stock")
    predictions = relationship("Prediction", back_populates="stock")

class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    title = Column(String(200))
    content = Column(Text)
    summary = Column(Text)
    source = Column(String(100))
    published_at = Column(DateTime)
    sentiment_score = Column(Float)
    
    stock = relationship("Stock", back_populates="news")

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    predicted_price = Column(Float)
    prediction_date = Column(DateTime)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    stock = relationship("Stock", back_populates="predictions") 