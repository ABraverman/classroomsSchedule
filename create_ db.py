import sqlite3
import os.path
import sys

_conn = 0


def create_tables():
    if not os.path.isfile("schedule.db"):
        _conn = sqlite3.connect("schedule.db")
        _conn.executescript("""
        CREATE TABLE courses (
            id                  INTEGER     PRIMARY KEY 
            course_name         TEXT        NOT NULL
            student             TEXT        NOT NULL
            number_of_students  INTEGER     NOT NULL
            class_id            INTEGER     REFERENCES classrooms(id)
            course_length       INTEGER     NOT NULL
        );
 
        CREATE TABLE students (
            grade   TEXT    PRIMARY KEY 
            count   INTEGER NOT NULL
        );
 
        CREATE TABLE classrooms (
            id                          INTEGER     PRIMARY KEY ,
            location                    TEXT        NOT NULL,
            current_course_id           INTEGER     NOT NULL DEFAULT 0,
            current_course_time_left    INTEGER     NOT NULL DEFAULT 0,
        );
        """)
        return 1
    else:
        return 0


def insert_course(arg):
    _conn.execute("""
    INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length) VALUES {}
    """.format(", ".join(arg)))


def insert_student(arg):
    _conn.execute("""
        INSERT INTO students (grade, count) VALUES {}
    """.format(", ".join(arg)))


def insert_classroom(arg):
    _conn.execute("""
    INSERT INTO classrooms (id,location) VALUES {}
    """.format(", ".join(arg)))


def main(args):
    if create_tables() == 1:
        config = open(args[1], "r")
        for line in config.readlines():
            arg = line.split(", ")
            if arg[0] == "C":
                insert_course(arg[1:])
            elif arg[0] == "S":
                insert_student(arg[1:])
            elif arg[0] == "R":
                insert_classroom(arg[1:])


if __name__ == '__main__':
    main(sys.argv)


