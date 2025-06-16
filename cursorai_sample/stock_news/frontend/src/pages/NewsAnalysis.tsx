import React from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Chip,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getStockNews } from '../api';
import { format } from 'date-fns';

interface NewsItem {
  id: number;
  title: string;
  content: string;
  summary: string;
  published_at: string;
  sentiment_score: number;
  source: string;
}

const NewsAnalysis: React.FC = () => {
  const { symbol } = useParams<{ symbol: string }>();

  const { data: news, isLoading } = useQuery<NewsItem[]>({
    queryKey: ['news', symbol],
    queryFn: () => getStockNews(symbol || ''),
    enabled: !!symbol,
  });

  const getSentimentColor = (score: number) => {
    if (score > 0.5) return '#4caf50';
    if (score < -0.5) return '#f44336';
    return '#ff9800';
  };

  const getSentimentLabel = (score: number) => {
    if (score > 0.5) return '긍정적';
    if (score < -0.5) return '부정적';
    return '중립적';
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {symbol} 관련 뉴스 분석
      </Typography>

      <Grid container spacing={3}>
        {news?.map((item) => (
          <Grid item xs={12} key={item.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" mb={2}>
                  <Typography variant="h6">{item.title}</Typography>
                  <Chip
                    label={getSentimentLabel(item.sentiment_score)}
                    style={{
                      backgroundColor: getSentimentColor(item.sentiment_score),
                      color: 'white',
                    }}
                  />
                </Box>
                <Typography color="textSecondary" gutterBottom>
                  {format(new Date(item.published_at), 'yyyy년 MM월 dd일 HH:mm')} |{' '}
                  {item.source}
                </Typography>
                <Typography variant="body1" paragraph>
                  {item.summary}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  감성 점수: {item.sentiment_score.toFixed(2)}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default NewsAnalysis; 