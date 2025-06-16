import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'

interface Prediction {
  current_price: number
  ma5: number
  ma20: number
  rsi: number
  sentiment: 'positive' | 'negative' | 'neutral'
  prediction_summary: string
}

const PredictionSection = () => {
  const { symbol } = useParams<{ symbol: string }>()
  const [prediction, setPrediction] = useState<Prediction | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        setLoading(true)
        const response = await axios.get(`http://localhost:8000/api/predictions/${symbol}`)
        setPrediction(response.data)
        setError('')
      } catch (err) {
        setError('예측 정보를 불러오는데 실패했습니다.')
        console.error('Error fetching prediction:', err)
      } finally {
        setLoading(false)
      }
    }

    if (symbol) {
      fetchPrediction()
    }
  }, [symbol])

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  if (!prediction) {
    return <div className="error">예측 정보를 찾을 수 없습니다.</div>
  }

  return (
    <div className="prediction-card">
      <h2 className="prediction-header">주가 분석</h2>
      
      <div className="stock-details">
        <div className="detail-item">
          <div className="detail-label">현재가</div>
          <div className="detail-value">${prediction.current_price.toFixed(2)}</div>
        </div>
        <div className="detail-item">
          <div className="detail-label">5일 이동평균</div>
          <div className="detail-value">${prediction.ma5.toFixed(2)}</div>
        </div>
        <div className="detail-item">
          <div className="detail-label">20일 이동평균</div>
          <div className="detail-value">${prediction.ma20.toFixed(2)}</div>
        </div>
        <div className="detail-item">
          <div className="detail-label">RSI</div>
          <div className="detail-value">{prediction.rsi.toFixed(2)}</div>
        </div>
      </div>

      <div className="sentiment-indicator">
        <div className="detail-label">뉴스 감성 분석:</div>
        <div className={`sentiment-${prediction.sentiment}`}>
          {prediction.sentiment === 'positive' && '긍정적 🟢'}
          {prediction.sentiment === 'negative' && '부정적 🔴'}
          {prediction.sentiment === 'neutral' && '중립적 🟡'}
        </div>
      </div>

      <div className="prediction-summary">
        <h3>분석 요약</h3>
        <p>{prediction.prediction_summary}</p>
      </div>
    </div>
  )
}

export default PredictionSection 