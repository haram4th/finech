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
import { getPricePrediction } from '../api';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { format } from 'date-fns';

interface PredictionData {
  date: string;
  actual_price?: number;
  predicted_price: number;
  confidence_score: number;
}

const PricePrediction: React.FC = () => {
  const { symbol } = useParams<{ symbol: string }>();

  const { data: predictions, isLoading } = useQuery<PredictionData[]>({
    queryKey: ['predictions', symbol],
    queryFn: () => getPricePrediction(symbol || ''),
    enabled: !!symbol,
  });

  const { data: accuracy } = useQuery<number>({
    queryKey: ['accuracy', symbol],
    queryFn: async () => {
      const response = await axios.get(`/api/predictions/${symbol}/accuracy`);
      return response.data;
    },
  });

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
        {symbol} 주가 예측
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                예측 정확도: {(accuracy || 0) * 100}%
              </Typography>
              <Box sx={{ height: 400 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={predictions}
                    margin={{
                      top: 5,
                      right: 30,
                      left: 20,
                      bottom: 5,
                    }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="date"
                      tickFormatter={(date) =>
                        format(new Date(date), 'MM/dd')
                      }
                    />
                    <YAxis />
                    <Tooltip
                      labelFormatter={(date) =>
                        format(new Date(date), 'yyyy년 MM월 dd일')
                      }
                    />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="actual_price"
                      stroke="#8884d8"
                      name="실제 가격"
                      strokeWidth={2}
                    />
                    <Line
                      type="monotone"
                      dataKey="predicted_price"
                      stroke="#82ca9d"
                      name="예측 가격"
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                예측 상세 정보
              </Typography>
              <Grid container spacing={2}>
                {predictions?.map((prediction) => (
                  <Grid item xs={12} sm={6} md={4} key={prediction.date}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="subtitle1">
                          {format(new Date(prediction.date), 'yyyy년 MM월 dd일')}
                        </Typography>
                        <Typography>
                          예측 가격: ${prediction.predicted_price.toFixed(2)}
                        </Typography>
                        <Typography>
                          신뢰도: {(prediction.confidence_score * 100).toFixed(1)}%
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PricePrediction; 