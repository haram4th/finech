import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'

interface NewsItem {
  headline: string
  summary: string
  datetime: number
  url: string
}

interface NewsSummary {
  summary: string
  original_news: NewsItem[]
}

const NewsSection = () => {
  const { symbol } = useParams<{ symbol: string }>()
  const [news, setNews] = useState<NewsSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true)
        const response = await axios.get(`http://localhost:8000/api/news/${symbol}/summary`)
        setNews(response.data)
        setError('')
      } catch (err) {
        setError('뉴스를 불러오는데 실패했습니다.')
        console.error('Error fetching news:', err)
      } finally {
        setLoading(false)
      }
    }

    if (symbol) {
      fetchNews()
    }
  }, [symbol])

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  if (!news) {
    return <div className="error">뉴스를 찾을 수 없습니다.</div>
  }

  return (
    <div>
      <div className="news-card">
        <h2>뉴스 요약</h2>
        <p className="news-summary">{news.summary}</p>
      </div>

      <h3>최근 뉴스</h3>
      {news.original_news.map((item, index) => (
        <div key={index} className="news-card">
          <h4 className="news-header">
            <a href={item.url} target="_blank" rel="noopener noreferrer">
              {item.headline}
            </a>
          </h4>
          <p className="news-summary">{item.summary}</p>
          <div className="news-meta">
            <span>{new Date(item.datetime * 1000).toLocaleDateString()}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default NewsSection 