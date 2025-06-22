import sqlite3 as sq

from CONSTANTS import DATABASE

def plus_enter(date):
    date = "-".join(date.split("_")[1:])

    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()
    cur.execute("UPDATE dates SET enters = enters + 1 WHERE date = ?", (date,))
    db.commit()
    cur.close()
    db.close()

def give_stat(date):
    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()
    cur.execute("SELECT enters FROM dates where date = ?", (date,))
    dates = cur.fetchall()
    cur.close()
    db.close()
    return dates

