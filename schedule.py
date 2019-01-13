import sqlite3
import os.path


def main():
    if os.path.isfile("schedule.db"):
        _conn = sqlite3.connect("schedule.db")

        cursor = _conn.cursor()
        counter = 0
        while True:
            cursor.execute("""
            SELECT classrooms.*, courses.course_name, courses.course_length FROM classrooms LEFT JOIN courses ON classrooms.current_course_id = courses.id
            """)
            rooms = cursor.fetchall()
            for i in rooms:
                if i[2] == 0:
                    cursor.execute("""
                    SELECT * FROM courses WHERE class_id = ?
                    """, [i[0]])
                    course = cursor.fetchone()
                    if course != None:
                        cursor.execute("""
                        SELECT * FROM students WHERE grade = ?
                        """, [course[2]])
                        student = cursor.fetchone()
                        if student[1] >= course[3]:
                            cursor.execute("""
                            UPDATE classrooms
                            SET current_course_id = ?, current_course_time_left = ?
                            WHERE id = ?
                            """, [course[0], course[5], i[0]])
                            cursor.execute("""
                            UPDATE students
                            SET count = count - ?
                            WHERE grade = ?
                            """, [course[3], course[2]])
                            print("(" + str(counter) + ") " + i[1] + ": " + course[1] + " is schedule to start")
                elif i[3] - 1 > 0:
                    print("(" + str(counter) + ") " + i[1] + ": occupied by " + i[4])
                    cursor.execute("""
                    UPDATE classrooms
                    SET current_course_time_left = current_course_time_left - 1
                    WHERE id = ?
                    """, [i[0]])
                else:
                    print("(" + str(counter) + ") " + i[1] + ": " + i[4] + " is done")
                    cursor.execute("""
                    DELETE FROM courses
                    WHERE id = ?
                    """, [i[2]])
                    cursor.execute("""
                    SELECT * FROM courses WHERE class_id = ?
                    """, [i[0]])
                    course = cursor.fetchone()
                    if course != None:
                        cursor.execute("""
                        UPDATE classrooms
                        SET current_course_id = ?, current_course_time_left = ?
                        WHERE id = ?
                        """, [course[0], course[5], i[0]])
                        cursor.execute("""
                        UPDATE students
                        SET count = count - ?
                        WHERE grade = ?
                        """, [course[3], course[2]])
                        print("(" + str(counter) + ") " + i[1] + ": " + course[1] + " is schedule to start")
                    else:
                        cursor.execute("""
                        UPDATE classrooms
                        SET current_course_id = 0, current_course_time_left = 0
                        WHERE id = ?
                        """, [i[0]])
            counter += 1
            cursor.execute("""
            SELECT * FROM courses 
            """)
            print_db(_conn.cursor())
            if len(cursor.fetchall()) <= 0:
                # _conn.commit()
                break



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


if __name__ == '__main__':
    main()





