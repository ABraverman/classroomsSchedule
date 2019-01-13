import sqlite3
import os.path
import sys

_conn = None


def create_tables():
    if not os.path.isfile("schedule.db"):
        global _conn
        _conn = sqlite3.connect("schedule.db")
        _conn.executescript("""
        CREATE TABLE courses (
            id                  INTEGER     PRIMARY KEY,
            course_name         TEXT        NOT NULL,
            student             TEXT        NOT NULL,
            number_of_students  INTEGER     NOT NULL,
            class_id            INTEGER     REFERENCES classrooms(id),
            course_length       INTEGER     NOT NULL
        );
 
        CREATE TABLE students (
            grade   TEXT    PRIMARY KEY,
            count   INTEGER NOT NULL
        );
 
        CREATE TABLE classrooms (
            id                          INTEGER     PRIMARY KEY ,
            location                    TEXT        NOT NULL,
            current_course_id           INTEGER     NOT NULL DEFAULT 0,
            current_course_time_left    INTEGER     NOT NULL DEFAULT 0
        );
        """)
        return True
    else:
        return False


def insert_course(arg):
    _conn.execute("""
    INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length) VALUES (?, ?, ?, ?, ?, ?)
    """, arg)


def insert_student(arg):
    _conn.execute("""
        INSERT INTO students (grade, count) VALUES (?, ?)
    """, arg)


def insert_classroom(arg):
    _conn.execute("""
    INSERT INTO classrooms (id,location) VALUES (?, ?)
    """, arg)


def print_db(cur):
    print("courses")
    cur.execute("""
            SELECT * FROM courses""")
    for i in cur.fetchall():
        print(i)
    print("classrooms")
    cur.execute("""
            SELECT * FROM classrooms""")
    for i in cur.fetchall():
        print(i)
    print("students")
    cur.execute("""
            SELECT * FROM students""")
    for i in cur.fetchall():
        print(i)




def main(args):
    if create_tables() == True:
        with open(args[1], "r") as config:
            for line in config.read().splitlines():
                arg = line.split(", ")
                if arg[0] == "C":
                    insert_course(arg[1:])
                elif arg[0] == "S":
                    insert_student(arg[1:])
                elif arg[0] == "R":
                    insert_classroom(arg[1:])
        print_db(_conn.cursor())
        _conn.commit()
        _conn.close()



if __name__ == '__main__':
    main(sys.argv)


