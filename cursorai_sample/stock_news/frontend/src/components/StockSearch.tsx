import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface StockSearchProps {
  onSymbolSelect: (symbol: string) => void
}

const StockSearch: React.FC<StockSearchProps> = ({ onSymbolSelect }) => {
  const [symbol, setSymbol] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (symbol.trim()) {
      onSymbolSelect(symbol.toUpperCase())
      navigate(`/stock/${symbol.toUpperCase()}`)
    }
  }

  return (
    <div className="search-container">
      <h1>주식 검색</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="search-input"
          placeholder="주식 심볼을 입력하세요 (예: AAPL)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <button type="submit" className="search-button">
          검색
        </button>
      </form>
      <div className="popular-symbols">
        <h3>인기 종목</h3>
        <div className="symbol-list">
          {['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'].map((sym) => (
            <button
              key={sym}
              className="symbol-button"
              onClick={() => {
                setSymbol(sym)
                onSymbolSelect(sym)
                navigate(`/stock/${sym}`)
              }}
            >
              {sym}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default StockSearch 