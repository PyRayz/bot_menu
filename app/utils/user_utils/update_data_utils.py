import os

import wget

import datetime

from CONSTANTS import PATH_FOLDER
def clear_folder():
    for filename in sorted(os.listdir(PATH_FOLDER)):
        file_path = os.path.join(PATH_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_days():
    for day in range(30):
        yield datetime.date.today() + datetime.timedelta(days=day)

def update_data():
    clear_folder()

    days = get_days()

    for day in days:
        url = f"https://foodmonitoring.ru/17031/food/{day}-sm.xlsx"

        try:
            wget.download(url=url, out=PATH_FOLDER)
        except:
            pass