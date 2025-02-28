# 1.학생번호, 학생명, 키높이, 학과번호, 학과명 정보를 출력하세요.
select * from student;   # N
select * from department; # 1
select student_id, student_name, height, d.department_id, department_name from student s LEFT JOIN department d
ON s.department_id = d.department_id;

# 2. 가교수 의 교수아이디를 출력하세요.
select professor_id from professor where professor_name='가교수';

# 3. 학과이름별 교수의 수를 출력하세요. group by , count(professor_id)
select * from professor;
select * from department;
select * from professor p LEFT JOIN department d
ON p.department_id = d.department_id;

select department_name, count(professor_id) 
from professor p LEFT JOIN department d
ON p.department_id = d.department_id GROUP BY d.department_name;

# 4. '정보통신공학'과의 학생정보를 출력하세요. 
select student_id, student_name, height, s.department_id, department_name from student s LEFT JOIN department d
ON s.department_id = d.department_id where department_name="정보통신학";

# 5. '정보통신공학'과의 교수명을 출력하세요.
select * from professor;
select * from department;
select * from professor p LEFT JOIN department d
ON p.department_id = d.department_id;
select professor_id, professor_name, p.department_id, department_name from professor p LEFT JOIN department d
ON p.department_id = d.department_id where department_name="정보통신학";

# 6. 학생 중 성이 '아'인 학생이 속한 학과명과 학생명을 출력하세요.
select * from student s LEFT JOIN department d
ON s.department_id = d.department_id WHERE student_name LIKE "아%";
select student_name, department_name from student s LEFT JOIN department d
ON s.department_id = d.department_id WHERE student_name LIKE "아%";

# 7. 키가 180~190사이에 속하는 학생 수를 출력하세요.
select count(student_id) from student where height between 180 and 190;

# 8. 학과 이름별 키의 최고값, 평균값을 출력하세요.
# group by department_name, max(height), avg(height)
select * from student s LEFT JOIN department d
on s.department_id = d.department_id;

select department_name, max(height), round(avg(height)) 
from student s LEFT JOIN department d
on s.department_id = d.department_id group by department_name;

# 9. '다길동' 학생과 같은 학과에 속한 학생의 이름을 출력하세요.
select * from student where student_name='다길동';
select student_name from student where department_id=1;

# 서브쿼리 1개의 sql 문장 안에 select 문이 2개 이상 
select student_name from student where department_id=(select department_id from student where student_name='다길동');

# 10. 2016년 11월 시작하는 과목을 수강하는 학생의 이름과 수강과목을 출력하세요.
select * from student;
select * from course;
select * from student_course;
select student_name, course_name from student s LEFT JOIN student_course sc
ON s.student_id =  sc.student_id
LEFT JOIN course c ON sc.course_id = c.course_id
WHERE start_date like "2016-11%";

# 11. '데이터베이스 입문' 과목을 수강신청한 학생의 이름은?
select student_name from student s LEFT JOIN student_course sc
ON s.student_id =  sc.student_id
LEFT JOIN course c ON sc.course_id = c.course_id 
where course_name='데이터베이스 입문';

# 12. '빌게이츠' 교수의 과목을 수강신청한 학생수는?
select * from professor p LEFT JOIN course c
on p.professor_id = c.professor_id
where professor_name='빌게이츠';  # course_id = 4

select course_id from professor p LEFT JOIN course c
on p.professor_id = c.professor_id
where professor_name='빌게이츠';

select count(*) from student s LEFT JOIN student_course sc
ON s.student_id=sc.student_id 
where course_id=(select course_id from professor p LEFT JOIN course c
on p.professor_id = c.professor_id
where professor_name='빌게이츠');

