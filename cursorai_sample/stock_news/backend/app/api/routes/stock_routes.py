from fastapi import APIRouter, HTTPException
from app.services.stock_service import StockService
from typing import List
from pydantic import BaseModel

router = APIRouter()
stock_service = StockService()

class StockData(BaseModel):
    symbol: str
    company_name: str
    current_price: float
    change_percent: float
    market_cap: float
    volume: int
    pe_ratio: float
    dividend_yield: float

class StockSearchResult(BaseModel):
    symbol: str
    company_name: str
    current_price: float

@router.get("/search", response_model=List[StockSearchResult])
async def search_stocks(query: str):
    try:
        return await stock_service.search_stocks(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}", response_model=StockData)
async def get_stock_info(symbol: str):
    try:
        return await stock_service.get_stock_info(symbol)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Stock not found: {str(e)}")

@router.get("/{symbol}/price")
async def get_stock_price(symbol: str):
    try:
        stock_service = StockService()
        return await stock_service.get_stock_price(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 