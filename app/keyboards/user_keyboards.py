from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import datetime

from app.utils.user_utils.reformators_utils import *

async def main():
    main = InlineKeyboardBuilder()

    for dates in zip(date_to_str(), get_callback_days()):
        text = "Сегодня" if get_reform_date(dates[1]) == str(datetime.date.today()) else ("Завтра" if get_reform_date(dates[1]) == str(datetime.date.today() + datetime.timedelta(days=1)) else dates[0])
        main.add(InlineKeyboardButton(text=text, callback_data=dates[1]))


    return (main.adjust(3).as_markup(), main)

back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад🔙", callback_data="back")]])

ad = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="НАПИСАТЬ🚀", url="https://t.me/Xillles")]])
