import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Button,
} from '@mui/material';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const symbol = location.pathname.split('/')[2];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{ textDecoration: 'none', color: 'white', flexGrow: 1 }}
          >
            주식 뉴스 분석기
          </Typography>
          {symbol && (
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button
                color="inherit"
                component={Link}
                to={`/stock/${symbol}`}
              >
                주식 정보
              </Button>
              <Button
                color="inherit"
                component={Link}
                to={`/news/${symbol}`}
              >
                뉴스 분석
              </Button>
              <Button
                color="inherit"
                component={Link}
                to={`/prediction/${symbol}`}
              >
                가격 예측
              </Button>
            </Box>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ flex: 1, py: 4 }}>
        {children}
      </Container>
    </Box>
  );
};

export default Layout; 