USE ddz2pt_db;

SELECT students.name, students.major, grades.course, grades.grade
FROM students
JOIN grades ON students.student_id = grades.student_id
WHERE grades.grade = 'A';