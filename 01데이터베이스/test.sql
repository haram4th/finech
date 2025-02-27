use korea_stock_info;
show tables;
select * from stock_company_info;
select * from 2024_08_stock_price_info;


CREATE TABLE stock_2024_all AS
SELECT * FROM 2024_07_stock_price_info
UNION ALL
SELECT * FROM 2024_08_stock_price_info
UNION ALL
SELECT * FROM 2024_09_stock_price_info;

use korea_stock_info;
select * from stock_2024_all;

select 회사명, max(현재가), min(현재가), avg(현재가), avg(변화율) from stock_2024_all group by 회사명;

SELECT 
    sp.회사명, ci.증권종류, ci.종목코드, ci.주요제품,
    MAX(sp.현재가) AS 최고가, 
    MIN(sp.현재가) AS 최저가, 
    AVG(sp.현재가) AS 평균가, 
    AVG(sp.변화율) AS 평균변화율
FROM stock_2024_all sp
INNER JOIN stock_company_info ci ON sp.회사명 = ci.회사명
GROUP BY sp.회사명
ORDER BY AVG(sp.변화율) DESC;