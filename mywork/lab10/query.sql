USE ddz2pt_db;

SELECT s.name, s.major, g.course, g.grade
FROM students s
JOIN grades g ON s.student_id = g.student_id
WHERE s.major = 'Computer Science';
