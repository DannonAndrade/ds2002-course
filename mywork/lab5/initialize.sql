USE ddz2pt_db;

DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    major VARCHAR(50),
    year INT
);

CREATE TABLE grades (
    grade_id INT PRIMARY KEY,
    student_id INT,
    course VARCHAR(50),
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

INSERT INTO students VALUES (1, 'Alice Smith', 'Computer Science', 2);
INSERT INTO students VALUES (2, 'Bob Jones', 'Biology', 3);
INSERT INTO students VALUES (3, 'Carol White', 'Math', 1);
INSERT INTO students VALUES (4, 'David Brown', 'History', 4);
INSERT INTO students VALUES (5, 'Eva Green', 'Computer Science', 2);
INSERT INTO students VALUES (6, 'Frank Lee', 'Biology', 3);
INSERT INTO students VALUES (7, 'Grace Kim', 'Math', 1);
INSERT INTO students VALUES (8, 'Henry Park', 'History', 4);
INSERT INTO students VALUES (9, 'Iris Chen', 'Computer Science', 3);
INSERT INTO students VALUES (10, 'Jake Moore', 'Biology', 2);

INSERT INTO grades VALUES (1, 1, 'DS2002', 'A');
INSERT INTO grades VALUES (2, 2, 'BIO101', 'B');
INSERT INTO grades VALUES (3, 3, 'MATH201', 'A');
INSERT INTO grades VALUES (4, 4, 'HIST101', 'C');
INSERT INTO grades VALUES (5, 5, 'DS2002', 'B');
INSERT INTO grades VALUES (6, 6, 'BIO101', 'A');
INSERT INTO grades VALUES (7, 7, 'MATH201', 'B');
INSERT INTO grades VALUES (8, 8, 'HIST101', 'A');
INSERT INTO grades VALUES (9, 9, 'DS2002', 'A');
INSERT INTO grades VALUES (10, 10, 'BIO101', 'C');