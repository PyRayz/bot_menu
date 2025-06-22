from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.admin_utils.dates.update_dates import get_dates

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Количество пользователей👤", callback_data="users_list")],
                     [InlineKeyboardButton(text="Статистика по датам📆", callback_data="dates")]])


async def dates():
    dates_mark_up = InlineKeyboardBuilder()
    dates_list = get_dates()

    for date in dates_list:
        dates_mark_up.add(InlineKeyboardButton(text=date[0], callback_data=date[0]))

    dates_mark_up.add(InlineKeyboardButton(text="Назад🔙", callback_data="back_admin_panel"))

    return (dates_mark_up.adjust(3).as_markup(), dates)


back_admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад🔙", callback_data="back_admin_panel")]])

back_dates_panel = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад🔙", callback_data="back_dates_panel")]])
