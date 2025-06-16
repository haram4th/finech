from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services import prediction_service
from app.schemas.predictions import PredictionResponse, PredictionCreate

router = APIRouter()

@router.get("/{symbol}", response_model=List[PredictionResponse])
async def get_stock_predictions(symbol: str, days: int = 7, db: Session = Depends(get_db)):
    """특정 주식의 향후 주가 예측을 가져옵니다."""
    try:
        predictions = await prediction_service.get_predictions(symbol, days, db)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{symbol}/generate", response_model=PredictionResponse)
async def generate_prediction(
    symbol: str,
    prediction_data: PredictionCreate,
    db: Session = Depends(get_db)
):
    """새로운 주가 예측을 생성합니다."""
    try:
        prediction = await prediction_service.create_prediction(
            symbol,
            prediction_data,
            db
        )
        return prediction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{symbol}/accuracy", response_model=float)
async def get_prediction_accuracy(symbol: str, db: Session = Depends(get_db)):
    """예측 모델의 정확도를 반환합니다."""
    try:
        accuracy = await prediction_service.get_model_accuracy(symbol, db)
        return accuracy
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 