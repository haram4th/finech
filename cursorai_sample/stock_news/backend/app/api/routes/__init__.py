from .stock_routes import router as stock_router
from .news_routes import router as news_router
from .prediction_routes import router as prediction_router

__all__ = ['stock_router', 'news_router', 'prediction_router'] 