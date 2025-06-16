import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'

interface StockInfo {
  symbol: string
  price: number
  change: number
  companyName: string
  marketCap: number
  volume: number
}

const StockDetail = () => {
  const { symbol } = useParams<{ symbol: string }>()
  const [stockInfo, setStockInfo] = useState<StockInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchStockInfo = async () => {
      try {
        setLoading(true)
        const response = await axios.get(`http://localhost:8000/api/stocks/${symbol}`)
        setStockInfo(response.data)
        setError('')
      } catch (err) {
        setError('주식 정보를 불러오는데 실패했습니다.')
        console.error('Error fetching stock info:', err)
      } finally {
        setLoading(false)
      }
    }

    if (symbol) {
      fetchStockInfo()
    }
  }, [symbol])

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  if (!stockInfo) {
    return <div className="error">주식 정보를 찾을 수 없습니다.</div>
  }

  return (
    <div className="stock-card">
      <div className="stock-header">
        <div className="stock-symbol">{stockInfo.symbol}</div>
        <div className="stock-price">
          ${stockInfo.price.toFixed(2)}
          <span className={`price-change ${stockInfo.change >= 0 ? 'positive' : 'negative'}`}>
            {stockInfo.change >= 0 ? '+' : ''}{stockInfo.change.toFixed(2)}%
          </span>
        </div>
      </div>
      
      <div className="stock-details">
        <div className="detail-item">
          <div className="detail-label">회사명</div>
          <div className="detail-value">{stockInfo.companyName}</div>
        </div>
        <div className="detail-item">
          <div className="detail-label">시가총액</div>
          <div className="detail-value">
            ${(stockInfo.marketCap / 1000000000).toFixed(2)}B
          </div>
        </div>
        <div className="detail-item">
          <div className="detail-label">거래량</div>
          <div className="detail-value">
            {(stockInfo.volume / 1000000).toFixed(2)}M
          </div>
        </div>
      </div>
    </div>
  )
}

export default StockDetail 