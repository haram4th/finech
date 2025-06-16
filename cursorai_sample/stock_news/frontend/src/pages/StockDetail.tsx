import React from 'react';
import { useParams } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
} from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getStockInfo } from '../api';

interface StockInfo {
  symbol: string;
  company_name: string;
  current_price: number;
  change_percent: number;
  market_cap: number;
  volume: number;
  pe_ratio: number;
  dividend_yield: number;
}

const StockDetail: React.FC = () => {
  const { symbol } = useParams<{ symbol: string }>();

  const { data: stockInfo, isLoading } = useQuery<StockInfo>({
    queryKey: ['stock', symbol],
    queryFn: () => getStockInfo(symbol || ''),
    enabled: !!symbol,
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center">
        <CircularProgress />
      </Box>
    );
  }

  if (!stockInfo) {
    return (
      <Typography variant="h5" color="error">
        주식 정보를 불러올 수 없습니다.
      </Typography>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {stockInfo.company_name} ({stockInfo.symbol})
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h3" gutterBottom>
                ${stockInfo.current_price.toFixed(2)}
                <Typography
                  component="span"
                  variant="h5"
                  color={stockInfo.change_percent >= 0 ? 'success.main' : 'error.main'}
                  sx={{ ml: 2 }}
                >
                  {stockInfo.change_percent >= 0 ? '+' : ''}
                  {stockInfo.change_percent.toFixed(2)}%
                </Typography>
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                기본 정보
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography color="textSecondary">시가총액</Typography>
                  <Typography variant="h6">
                    ${(stockInfo.market_cap / 1000000000).toFixed(2)}B
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="textSecondary">거래량</Typography>
                  <Typography variant="h6">
                    {(stockInfo.volume / 1000000).toFixed(2)}M
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                투자 지표
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography color="textSecondary">P/E 비율</Typography>
                  <Typography variant="h6">{stockInfo.pe_ratio.toFixed(2)}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="textSecondary">배당 수익률</Typography>
                  <Typography variant="h6">{stockInfo.dividend_yield.toFixed(2)}%</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StockDetail; 