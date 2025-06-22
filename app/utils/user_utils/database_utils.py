import sqlite3 as sq

from aiogram.types import Message

from CONSTANTS import DATABASE
def create_tables():
    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id STRING PRIMARY KEY)");
    cur.execute("CREATE TABLE IF NOT EXISTS dates(date TEXT PRIMARY KEY, enters INTEGER)");
    db.commit()
    cur.close()
    db.close()

def reg_user(message):
    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()
    cur.execute("INSERT OR IGNORE INTO users(id) VALUES(?)", (str(oct(message.from_user.id)),))
    db.commit()
    cur.close()
    db.close()