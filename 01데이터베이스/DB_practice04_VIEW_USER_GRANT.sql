# view 뷰   
# select로 조회한 내용을 테이블을 만드는 것처럼 저장하는 것.
# 읽기 전용
# CREATE VIEW 뷰이름 AS SELECT문
# DROP VIEW 뷰이름

USE korea_exchange_rate;
SELECT * FROM exchange_rate;

# 1997년 1월 1일부터 2001년 12월 31일까지 환율변동 조회
SELECT * FROM exchange_rate WHERE date 
between "1997-01-01" and "2001-12-31";

# 통화별로 현찰_살때_환율, 현찰_팔때_환율의
# MIN() 살때최저환율, MAX() 살때최고환율, AVG() 살때평균환율,
# MAX() - MIN() 살때환율변동량
# MIN() 팔때최저환율, MAX() 팔때최고환율, AVG() 팔때평균환율,
# MAX() - MIN() 팔때환율변동량

CREATE VIEW exchange_rate_1997_2001 AS
SELECT 통화, 
	MIN(현찰_살때_환율) 살때최저환율, 
    MAX(현찰_살때_환율) 살때최고환율, 
    round(AVG(현찰_살때_환율), 2) 살때평균환율, 
    round(MAX(현찰_살때_환율) - MIN(현찰_살때_환율), 2) 살때환율변동량,
    MIN(현찰_팔때_환율) 팔때최저환율, 
    MAX(현찰_팔때_환율) 팔때최고환율, 
    round(AVG(현찰_팔때_환율), 2) 팔때평균환율, 
    round(MAX(현찰_팔때_환율) - MIN(현찰_팔때_환율), 2) 팔때환율변동량
    FROM exchange_rate WHERE date 
between "1997-01-01" and "2001-12-31" 
GROUP BY 통화;

SELECT * FROM exchange_rate_1997_2001 WHERE 통화='미국 USD';

UPDATE exchange_rate_1997_2001 SET 통화='미국' WHERE 살때최저환율=855.34;
