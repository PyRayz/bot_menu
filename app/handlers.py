from aiogram import Bot, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, Chat

from app.utils.user_utils.database_utils import reg_user
from app.utils.admin_utils.users import count_rows
from app.utils.admin_utils.dates.dates import *
from app.utils.user_utils.basic_utils import *

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_RUNNING

from app.keyboards import admin_keyboards as kb_admin
from app.keyboards import user_keyboards as kb_user

schedule = AsyncIOScheduler(timezone="Europe/Moscow")

async def stop_scheduler():
    if schedule.state == STATE_RUNNING:
        schedule.shutdown()


bot = Bot(token=TOKEN)
router = Router()


# user handlers

@router.message(CommandStart())
async def start(message: Message):
    reg_user(message)

    result = await kb_user.main()

    if message.text == "/start":

        await message.answer(text="<b>РЕКЛАМА/ЗАКАЗАТЬ БОТА - @Xillles</b>", reply_markup=kb_user.ad,
                             parse_mode="HTML")

        await message.delete()

        if result[1].export():
            await message.answer(text=TEXT_ADD + TEXT, reply_markup=result[0])

            message_chat_id = message.chat.id
            message_id = message.message_id

        else:
            await message.answer(text=TEXT_VACATION)

            message_chat_id = message.chat.id
            message_id = message.message_id
    else:

        if result[1].export():
            await message.edit_text(text=TEXT, reply_markup=result[0])

            message_chat_id = message.chat.id
            message_id = message.message_id - 2

        else:
            await message.edit_text(text=TEXT_VACATION)

            message_chat_id = message.chat.id
            message_id = message.message_id - 2

    schedule.add_job(func=change_message, trigger="cron", hour=0, minute=1,
                     args=(bot, message_chat_id, message_id))


    try:
        schedule.start()
    except:
        pass

@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await start(callback.message)


@router.callback_query(F.data.startswith("_"))
async def get_menu(callback: CallbackQuery):
    try:
        await stop_scheduler()
    except:
        pass

    data = get_data(callback.data)

    text = "На этот день, <b>ОПИРАЯСЬ НА САЙТ ШКОЛЫ*</b> в столовой дают следующее:\n\n"

    for category, dish in data.items():
        text += f"<b>{category}</b> - <i>{dish}</i>\n\n"

    text += """<i>ПРИЯТНОГО АППЕТИТА!</i>\n
<b>*Информация была взята из сайта школы и иногда может не соответствовать действительности</b>\n"""

    await callback.message.edit_text(text=text, reply_markup=kb_user.back, parse_mode="HTML")

    plus_enter(callback.data)


# admin handlers
@router.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id != ADMIN:
        await bot.delete_message(message.chat.id, message.message_id)
    else:

        if message.text == "/admin":
            await message.delete()
            await message.answer(text="<b>Это администраторская панель💻\n\n"
                                         "Здесь вы можете отслеживать статистику и количество пользователей бота</b>\n\n"
                                         "Выберите функцию👇", reply_markup=kb_admin.admin_panel, parse_mode="HTML")

        else:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="<b>Это администраторская панель💻\n\n"
                                         "Здесь вы можете отслеживать статистику и количество пользователей бота</b>\n\n"
                                         "Выберите функцию👇", reply_markup=kb_admin.admin_panel, parse_mode="HTML")


@router.callback_query(F.data == "users_list")
async def users_list(callback: CallbackQuery):
    count_users = count_rows()
    await callback.message.edit_text(text=f"<b>Количество пользователей: {count_users}👤</b>",
                                     reply_markup=kb_admin.back_admin_panel, parse_mode="HTML")


@router.callback_query(F.data == "dates")
async def dates_list(callback: CallbackQuery):
    result = await kb_admin.dates()
    await callback.message.edit_text(text="Выберите дату на которую хотите узнать статистику\n\n"
                                     "<b>*Статистика хранится на последние 10 дат</b>", reply_markup=result[0],
                                     parse_mode="HTML")


@router.callback_query(F.data == "back_admin_panel")
async def back_admin_panel(callback: CallbackQuery):
    message = Message(
        message_id=callback.message.message_id,
        from_user=callback.from_user,
        chat=Chat(id=callback.message.chat.id, type=callback.message.chat.type),
        date=callback.message.date,
        text=callback.message.text
    )

    await admin(message)


@router.callback_query(F.data == "back_dates_panel")
async def back_dates_panel(callback: CallbackQuery):
    await dates_list(callback)


@router.callback_query(F.data)
async def give_statistic(callback: CallbackQuery):
    users = give_stat(callback.data)

    await callback.message.edit_text(text=f"<b>{users[0][0]} раз(а) заходили на этот день, чтобы посмотреть меню</b>",
                                  parse_mode="HTML", reply_markup=kb_admin.back_dates_panel)


# delete messages
@router.message(Command("/"))
async def del_mess(message: Message):
    await bot.delete_message(message.chat.id, message.message_id)


@router.message()
async def del_mess(message: Message):
    await bot.delete_message(message.chat.id, message.message_id)
