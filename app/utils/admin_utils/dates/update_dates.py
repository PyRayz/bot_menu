import sqlite3 as sq

import os

from CONSTANTS import *

def get_dates():
    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()
    cur.execute("SELECT date FROM dates")
    dates = cur.fetchall()
    cur.close()
    db.close()
    return dates

def clear_dates():
    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()
    dates_list = get_dates()

    if len(dates_list) >= 10:
        while len(dates_list) > 9:
            cur.execute(f"DELETE FROM dates WHERE date = ?", (dates_list[0][0], ))
            db.commit()
            dates_list = get_dates()

    cur.close()
    db.close()

def get_reform_dates():
    basic_dates = sorted(os.listdir(PATH_FOLDER))

    del basic_dates[-1]

    reformed_dates = []

    for date in basic_dates:
        date = date.split("-")

        del date[-1]

        date = "-".join(date)

        reformed_dates.append(date)

    return reformed_dates

def enter_data(dates, file_dates):
    db = sq.connect(DATABASE, timeout=1)
    cur = db.cursor()

    for date in file_dates:
        if len(dates) < 10:
            cur.execute("INSERT OR IGNORE INTO dates(date, enters) VALUES(?, 0)", (date,))
            db.commit()
            dates = get_dates()
        else:
            break

    cur.close()
    db.close()

def update_dates():
    dates = get_dates()
    file_dates = get_reform_dates()

    if file_dates:
        if dates:
            if dates[-1] != file_dates[-1]:
                clear_dates()

                enter_data(dates, file_dates)
        else:
            enter_data(dates, file_dates)