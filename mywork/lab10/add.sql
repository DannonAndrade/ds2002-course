USE ddz2pt_db;

-- Add 2 new students
INSERT INTO students VALUES (11, 'Kevin Hart', 'Physics', 2);
INSERT INTO students VALUES (12, 'Lily Adams', 'Chemistry', 1);

-- Add 3 new grades (linked to valid student_ids)
INSERT INTO grades VALUES (11, 11, 'PHYS101', 'A');
INSERT INTO grades VALUES (12, 12, 'CHEM101', 'B');
INSERT INTO grades VALUES (13, 11, 'MATH201', 'A');
