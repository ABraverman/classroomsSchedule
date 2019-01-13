import sqlite3
import os
import sys
import create_db

sys.argv.append("config")

create_db.main(sys.argv)

_conn = sqlite3.connect("schedule.db")
cursor = _conn.cursor()

cursor.execute("""
SELECT *
FROM  students
""")
print("\n\n{}".format(cursor.fetchall()))
i = 6
cursor.execute("""
UPDATE students
SET count = count - ?
WHERE grade = 'cs_undgrad'
""", [i])
cursor.execute("""
SELECT *
FROM  students
""")
print(cursor.fetchall())

os.remove("schedule.db")