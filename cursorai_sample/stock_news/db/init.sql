CREATE DATABASE IF NOT EXISTS stocknews;
USE stocknews;

-- 주식 테이블
CREATE TABLE IF NOT EXISTS stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    company_name VARCHAR(100) NOT NULL,
    current_price DECIMAL(10, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_symbol (symbol)
);

-- 뉴스 테이블
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    summary TEXT,
    source VARCHAR(100),
    published_at TIMESTAMP,
    sentiment_score DECIMAL(4, 3),
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    INDEX idx_stock_date (stock_id, published_at)
);

-- 예측 테이블
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    predicted_price DECIMAL(10, 2) NOT NULL,
    prediction_date DATE NOT NULL,
    confidence_score DECIMAL(4, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (stock_id) REFERENCES stocks(id),
    INDEX idx_stock_date (stock_id, prediction_date)
); 