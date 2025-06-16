import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import theme from './theme';
import Layout from './components/Layout';
import StockSearch from './pages/StockSearch';
import StockDetail from './pages/StockDetail';
import NewsAnalysis from './pages/NewsAnalysis';
import PricePrediction from './pages/PricePrediction';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<StockSearch />} />
              <Route path="/stock/:symbol" element={<StockDetail />} />
              <Route path="/news/:symbol" element={<NewsAnalysis />} />
              <Route path="/prediction/:symbol" element={<PricePrediction />} />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App; 