from fastapi import APIRouter, HTTPException
from app.services.prediction_service import PredictionService
from typing import List
from pydantic import BaseModel
from datetime import date

router = APIRouter()
prediction_service = PredictionService()

class PredictionData(BaseModel):
    date: date
    actual_price: float | None
    predicted_price: float
    confidence_score: float

@router.get("/{symbol}", response_model=List[PredictionData])
async def get_price_predictions(symbol: str):
    try:
        return await prediction_service.get_price_predictions(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/accuracy")
async def get_prediction_accuracy(symbol: str):
    try:
        return await prediction_service.get_prediction_accuracy(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 