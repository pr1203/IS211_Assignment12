DROP TABLE IF EXISTS `Students`;
CREATE TABLE `Students`(
    student_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
    );

DROP TABLE IF EXISTS `Quizzes`;
CREATE TABLE `Quizzes`(
    quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    number_of_questions INT NOT NULL,
    quiz_date DATE NOT NULL
    );

DROP TABLE IF EXISTS `Quiz_Results`;
CREATE TABLE `Quiz_Results`(
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL
    );

INSERT INTO 'Students' (student_id, first_name, last_name) VALUES
(1, 'John', 'Smith');

INSERT INTO 'Quizzes' (quiz_id, subject, number_of_questions, quiz_date) VALUES
(1, 'Python Basics', 5, '2015-05-05');

INSERT INTO 'Quiz_Results' (result, quiz_id, student_id) VALUES
(85, 1, 1);
