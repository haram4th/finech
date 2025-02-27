use korea_stock_info;
show tables;
select * from stock_company_info;
select * from 2024_09_stock_price_info limit 1000;
USE korea_exchange_rate;
show tables;
select count(*) from exchange_rate;

# 2020년 1월1일부터 12월 31까지 데이터에서 통화별 
# 현찰_살때_환율의 최소 min(), 최대 max(), 평균가avg()
select 통화, min(현찰_살때_환율) 최저가, max(현찰_살때_환율) 최고가, 
round(avg(현찰_살때_환율), 2) 평균가
from exchange_rate 
where date >= "2020-01-01" 
and date <= "2020-12-31" group by 통화;  

use korea_stock_info;
show tables;
select * from 2024_07_stock_price_info;
select * from 2024_08_stock_price_info;

# 7, 8, 9월로 나눠져 있는 데이터를 1개의 테이블로 모으기 위해서는 
# JOIN을 쓸 수 없으므로 UNION을 사용

create table stock_2024_all AS
select * from 2024_07_stock_price_info
UNION ALL
select * from 2024_08_stock_price_info
UNION ALL
select * from 2024_09_stock_price_info;

##################################################

# SQL 함수
# SELECT 함수(값)   MIN(), MAX()

# 절대값 ABS()
SELECT ABS(-34), ABS(1), ABS(-256);

# 문자열의 길이 측정: LENGTH(문자열);
SELECT LENGTH("3	47	14:25:59	SElECT ABS(-34), ABS(1), ABS(-256)
 LIMIT 0, 50000	1 row(s) returned	0.000 sec / 0.000 sec");
 
# 반올림 함수 round()
SELECT round(3.14567, 2);
SELECT round(3.14467, 2);

# 올림 ceil, 내림 floor
select ceil(4.1);
select floor(4.9);

# 연산자를 통한 계산 +, -, *, /, %(나머지), div(몫), mod(나머지)
select 7/2;
select 7*2;
select 7+2;
select 7-2;
select 7%2;
select 7 div 2;
select 7 mod 2;

# power(제곱), sqrt(루트), sign(음수양수) 확인
select power(4, 3); 
select sqrt(3);
select sign(3), sign(-78);

# truncate(값, 자릿수) 버림
select round(2.2345, 3), truncate(2.2345, 3);
select round(1153.2345, -2), truncate(1153.2345, -2);

# 문자열 함수
# 문자의 길이를 알아보는 함수
select char_length('my sql'), length('my sql');
select char_length('    '), length('호 길동');

# 문자를 연결하는 함수 concat(), concat_ws()
select concat('this', ' is ', 'mysql') as concat1;
select concat(' this', ' is ', 'mysql ') as concat1;
select concat(' this', null, 'mysql ') as concat1;
select concat_ws(' ', 'this', 'is', 'mysql') as concat3;
select concat_ws(' VS ', '헐크', '아이언맨', '타노스') as concat3;

# 대문자를 소문자로 lower(), 소문자를 대문자로 upper()
select lower('ABcd');
select upper('efgh'); 

# 문자열의 자릿수를 일정하게 하고 빈 공간을 지정한 문자로 채우는 함수
# lpad(값, 자릿수, 채울문자), rpad(값, 자릿수, 채울문자)
select lpad('sql', 7, "#");
select lpad('sql', 7, " ");
select lpad('sql', 7, "=");
select rpad('sql', 7, "#");
select rpad('sql', 7, " ");
select rpad('sql', 7, "=");

# 공백을 없애는 함수 ltrim(문자열), rtrim(문자열)
select ltrim('    SQL    ');
select rtrim('    SQL    ');

# 문자열의 공백을 앞 뒤로 삭제하는 trim()
select trim('    SQL    ');
select trim('    My SQL    ');
select trim('    My SQL STUDY   ');

# 문자열을 잘라내는 함수 left(문자열, 길이), right(문자열, 길이)
select left('this is my sql', 4), right('this is my sql', 5);
select left('이것이 mysql이다.', 5), right('이것이 mysql이다.', 5);

# 문자열을 중간에서 잘라내는 함수 substr(문자열, 시작위치, 길이)
select substr('this is my sql', 6, 5);
select substr('this is my sql', 6);

# 문자열의 공백을 앞 뒤로 삭제하고 문자열 앞 뒤에 포함된 특정 문자도 삭제하는 함수
# trim(leading '삭제할 문자' from, 전체 문자열);
select trim('    my sql    ');
select trim(leading '*' from '****my sql****');
select trim(trailing '*' from '****my sql****');
select trim(both '*' from '****my sql****');
select trim(both '*' from '****my * sql****');

# 날짜형 함수
select curdate(); # 현재 년월일 
select curtime(); # 현재 시간
select now(); #현재 년월일 + 현재 시간
select current_timestamp(); #현재 년월일 + 현재 시간

# 영문 요일 표시 함수 dayname(날짜)
select dayname(now());
select dayname("2025-12-25");

# 요일을 번호로 표시 
# dayofweek(날짜), 일(1), 월(2), 화(3), 수(4), 목(5), 금(6), 토(7)
select dayofweek(now());
select dayofweek("2024-5-5");

# 1년 중 오늘이 몇일째인지 dayofyear(날짜)
select dayofyear(now());
select dayofyear("2025-05-08");

# 날짜를 세분화 해서 보는 함수들
# 현재 달의 마지막 날이 몇 일까지 있는지 출력
select last_day(now());
select last_day("2025-10-01");

# 입력한 날짜에서 연도만 추출
select year(now());
select year("2025-10-01");

# 입력한 날짜에서 월만 출력
select month(now());
select month("2025-10-01");

# 입력한 날짜에서 월만 영문으로 출력
select monthname("2025-10-01");

# 몇 분기인기 출력
select quarter(now());
select quarter("2025-12-13");

# 몇 주차인지
select weekofyear(now());
select weekofyear("2025-12-25");

# 날짜와 시간이 같이 있는 데이터에서 날짜와 시간을 구분해주는 함수
select now();
select date(now());
select time(now());

# 날짜를 지정한 날 수 만큼 더하는 함수 
# date_add(날짜, interval 더할 날 수 day);
select date_add(now(), interval 5 day);
select adddate(now(), 5);

# 날짜를 지정한 날 수 만큼 빼는 함수 
# subdate(날짜, interval 뺄 날 수 day);
select subdate(now(), interval 5 day);
select subdate(now(), 5);

# 날짜와 시간을 년월, 날 시간, 분초 단위로 추출하는 함수
# extract(옵션, from 날짜시간)
select extract(year_month from now()); 
select extract(DAY_HOUR from now());
select extract(minute_second from now());

# 날짜 1에서 날짜 2를 뺀 일 수 계산
# datediff(날짜1, 날짜2)
select datediff(now(), '2024-12-25');

# 날짜 포멧 함수 -  지정한 형식에 맞춰서 출력해주는 함수
# %Y 4자리 연도, %y 2자리 연도
# %M 월의 영문표기, %m 2자리 월 표시, %b 월의 축약 영문표기 Jan, Feb
# %d 2자리 일 표기, %e 1자리 일 표기
select date_format(now(), '%d-%b-%Y');
select date_format(now(), '%d-%M-%Y');
select date_format(now(), '%e-%M-%Y');
select date_format("2025-01-01", '%e-%M-%Y');
select date_format("2025-01-01", '%d-%M-%Y');
select date_format("2025-01-01", '%d-%m-%y');

# 시간 표기
# %H 24시간, %h 12시간, %p AM, PM 표시
# %i 2자리 분 표기
# %S 2자리 초
# %T 24시간 표기법 시:분:초
# %r 12시간 표기법 시:분:초 AM/PM
# %W 요일의 영문표기, %w 숫자로 요일 표시 (일0, 월1, 화2, 수3, 목4, 금5, 토6)
select date_format(now(), '%H : %i : %S');
select date_format(now(), '%p %h : %i : %S');
select date_format(now(), '%T');
select date_format(now(), '%r');
select date_format(now(), '%W %r');
select date_format("2025-02-23 17:23:54", '%w %r');
select now();

select extract(DAY_HOUR from '2025-02-27 17:40:37') dayhour;
select now();
select extract(DAY_HOUR from now()) dayhour2; # now()와 같이 쓰면 오류남 시간만 표시됨