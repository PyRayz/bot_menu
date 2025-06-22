import os

from CONSTANTS import PATH_FOLDER, DATE_TO_STR

def get_callback_days():
    dates = sorted(os.listdir(PATH_FOLDER))

    dates.pop(-1)

    callback_dates = []

    if len(dates) > 10:
        while len(dates) != 10:
            dates.pop(-1)

    for date in dates:
        date = date.split("-")

        date.pop(-1)

        date = "_" + "_".join(date)

        callback_dates.append(date)

    return callback_dates

def date_to_str():
    old_dates = sorted(os.listdir(PATH_FOLDER))

    del old_dates[-1]

    new_dates = []

    if len(old_dates) > 10:
        while len(old_dates) != 10:
            del old_dates[-1]

    for date in old_dates:
        date = date.split("-")
        del date[-1]
        del date[0]
        date.reverse()

        date[1] = DATE_TO_STR[date[1]]

        date = " ".join(date)

        new_dates.append(date)

    return new_dates

def get_reform_date(date):
    date = date.split("_")

    del date[0]
    date = "-".join(date)

    return date