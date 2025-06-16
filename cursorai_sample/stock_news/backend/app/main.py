from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import stock_router, news_router, prediction_router

app = FastAPI(title="Stock News API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin을 지정해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(stock_router, prefix="/api/stocks")
app.include_router(news_router, prefix="/api/news")
app.include_router(prediction_router, prefix="/api/predictions")

@app.get("/")
async def root():
    return {"message": "Welcome to Stock News API"} 