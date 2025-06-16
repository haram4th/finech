import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { searchStocks } from '../api';

interface StockData {
  symbol: string;
  company_name: string;
  current_price: number;
}

const StockSearch: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const { data: stocks, isLoading } = useQuery<StockData[]>({
    queryKey: ['stocks', searchTerm],
    queryFn: () => searchStocks(searchTerm),
    enabled: searchTerm.length > 0,
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // 검색은 자동으로 실행됩니다
  };

  const handleStockClick = (symbol: string) => {
    navigate(`/stock/${symbol}`);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        주식 검색
      </Typography>
      <Box component="form" onSubmit={handleSearch} sx={{ mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={9}>
            <TextField
              fullWidth
              label="주식 심볼 또는 회사명 입력"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="예: AAPL, Apple"
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <Button
              fullWidth
              variant="contained"
              type="submit"
              sx={{ height: '100%' }}
            >
              검색
            </Button>
          </Grid>
        </Grid>
      </Box>

      {isLoading ? (
        <Box display="flex" justifyContent="center">
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={2}>
          {stocks?.map((stock) => (
            <Grid item xs={12} sm={6} md={4} key={stock.symbol}>
              <Card
                sx={{ 
                  cursor: 'pointer',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'scale(1.02)',
                  }
                }}
                onClick={() => handleStockClick(stock.symbol)}
              >
                <CardContent>
                  <Typography variant="h6">{stock.company_name}</Typography>
                  <Typography color="textSecondary">{stock.symbol}</Typography>
                  <Typography variant="h5" sx={{ mt: 2 }}>
                    ${stock.current_price.toFixed(2)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default StockSearch; 