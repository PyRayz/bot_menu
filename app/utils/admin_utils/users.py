import sqlite3 as sq
from CONSTANTS import DATABASE


def count_rows():
    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    count = cur.fetchall()
    cur.close()
    db.close()

    return len(count)
