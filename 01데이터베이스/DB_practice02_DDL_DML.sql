# 데이터베이스, 테이블 만들기
Create database sampleDB;
DROP database sampleDB;
# 데이터베이스 조회하기
SHOW databases;

# 테이블 만들기
USE sampledb;
# CREATE table 테이블명 (컬럼명1(데이터타입),  컬럼명2(데이터타입)...);
CREATE table customers(id int, name varchar(100),  sex varchar(20),
phone varchar(20), address varchar(255));

# 테이블 삭제하기
DROP table customers;

# market_db 만들기
Create database market_db;
USE market_db;

# hongong1 테이블 만들기 toy_id(int), toy_name(char(4)), age(int)
CREATE table hongong1 (toy_id int, toy_name char(4), age int); 
SHOW tables;
DESC hongong1;

# 생성한 테이블에 데이터 입력하기 INSERT INTO 테이블명(컬럼명1, 컬럼명2, 컬럼명3) VALUES (1, '우디', 25);
INSERT INTO hongong1(toy_id, toy_name, age) VALUES(1, "우디", 25);

SELECT * FROM hongong1;

# id: 2, name 버즈, 
INSERT INTO hongong1(toy_id, toy_name) VALUES(2, '버즈');

INSERT INTO hongong1(toy_name, age, toy_id) VALUES('제시', 20, 3);
INSERT INTO hongong1 VALUES(5, '포테이토', 40);
INSERT INTO hongong1 VALUES(6, '강아지');
INSERT INTO hongong1(toy_name, age) VALUES('강아지', 3);

# primary key와 auto increment기능을 추가한 테이블 만들기
CREATE TABLE hongong2 (
	toy_id int AUTO_INCREMENT PRIMARY KEY,
    toy_name char(4),
    age int);
    
DESC hongong2;

#  AUTO_INCREMENT가 지정된 테이블에 데이터 넣기
INSERT INTO hongong2 VALUES (NULL, '보핍', 25);
INSERT INTO hongong2 VALUES (NULL, '슬링키', 22);
INSERT INTO hongong2 VALUES (NULL, '렉스', 21);
SELECT * FROM hongong2;

# 테이블 수정하기 alter
# 컬럼 추가 ALTER TABLE 테이블명 ADD COLUMN 컬럼명, 자료형, 속성(NOT NULL, UNIQUE)
# hongong2 테이블에 country 컬럼 추가하기
ALTER TABLE hongong2 ADD COLUMN country varchar(100);

# 기존 테이블에 있는 자료 UPDATE 하기 where 와 함께 씀!!
# UPDATE 테이블명 SET 컬럼명 = 업데이트할 값 WHERE toy_id=1;
UPDATE hongong2 SET country='미국' WHERE toy_id=1;
UPDATE hongong2 SET age=30 WHERE toy_id=1;

# 테이블의 내용은 모두 지우고 테이블의 구조는 남기고 싶을 때 truncate
SELECT * FROM hongong1;
DESC hongong1;

# 테이블의 데이터 삭제 delete from 테이블명 where 조건
DELETE FROM hongong1 WHERE toy_id=2;

# idx 컬럼추가 primary key로 지정 AUTO_INCREMENT
ALTER TABLE hongong1 ADD COLUMN idx int AUTO_INCREMENT Primary Key;
DELETE FROM hongong1 WHERE idx=7;

INSERT INTO hongong1 VALUES(7, '렉스', 30, NULL);

# CREATE, INSERT, UPDATE, DELETE, (CRUD)


# 회원테이블, 제품테이블 만들기
CREATE TABLE member (
	id int AUTO_INCREMENT PRiMARY KEY,
    member_id varchar(20),
    name varchar(20),
    adddress varchar(255));
    
DESC member;

CREATE TABLE product(
	prod_name varchar(100),
    price int,
    date_of_prod varchar(20),
    manuf varchar(50),
    balance int);
    
DESC product;
DESC member;
INSERT INTO member 
VALUES (NULL, "tess", "나훈아", "경기 부천시 중동");
use market_db;
SELECT * FROM member;

# 여러개의 데이터 입력하기
INSERT INTO member 
VALUES (NULL, "hero", "임영웅", "서울 은평구 증산동"),
(NULL, "iyou", "아이유", "인천 남구 주안동"),
(NULL, "JYP", "박진영", "경기 고양시 장항동");

INSERT INTO product VALUES
	("바나나", 1500, "2024-07-01", "델몬트", 17),
    ("카스", 2500, "2023-12-12", "OB", 3),
	("삼각김밥", 1000, "2025-02-26", "CJ", 22);
    
SELECT * FROM product;

# product 테이블에 prod_id 컬럼을 추가하고 
# Auto_increment, Primary key를 추가하세요.
ALTER table product ADD COLUMN prod_id int auto_increment primary key;
DESC member;
INSERT INTO member values(null, 'akmu', '악동뮤지션', null);
INSERT INTO member (id, member_id, name)
values(null, 'akmu2', '악동뮤지션2');
select * from member;

# Rollback 연습
CREATE database mywork;
USE mywork;
CREATE table emp_test
(emp_no int not null,
emp_name varchar(30) not null,
hire_date date null,
salary int null,
primary key(emp_no));
DESC emp_test;
INSERT INTO emp_test
(emp_no, emp_name, hire_date, salary)
values
(1005, '퀴리', '2021-03-01', 4000),
(1006, '호킹', '2021-03-05', 5000),
(1007, '패러데이', '2021-04-01', 2200),
(1008, '맥스웰', '2021-04-04', 3300),
(1009, '플랑크', '2021-04-05', 4400);
SELECT * FROM emp_test;

# update 연습
# 호킹의 salary를 10000 으로 변경
# 패러데이의 hire_date를 2023-07-11 로 변경
# 플랑크가 있는 데이터를 삭제
UPDATE emp_test SET salary=10000 WHERE emp_no=1006;
UPDATE emp_test SET hire_date="2023-07-11" WHERE emp_no=1007;
DELETE FROM emp_test WHERE emp_no=1009;

# 오토커밋 옵션 활성화 확인
SELECT @@autocommit; # 결과가 1이면 오토커밋 활성화 0이면 비활성화
SET autocommit = 1;
SELECT @@autocommit;
select * from emp_test;
CREATE table emp_tran1 as select * from emp_test;
select * from emp_tran1;
DESC emp_tran1;
DESC emp_test;
ALTER TABLE emp_tran1 add constraint primary key(emp_no);
drop table emp_tran1;

show tables;
rollback;

select * from emp_test;
insert into emp_test values(1009, '플랑크', '2024-04-04', 5030);

select * from emp_test;
insert into emp_test values(1011, '플랑크4', '2024-04-05', 5000);commit;
insert into emp_test values(1012, '플랑크5', '2024-04-05', 5000);commit;
insert into emp_test values(1013, '플랑크6', '2024-04-05', 5000);
commit;
rollback;



