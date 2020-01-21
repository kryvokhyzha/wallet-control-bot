import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram import types

from app.Exceptions.NotCorrectMessage import NotCorrectMessage
import app.controllers.expense_controllers as expense_cnt
import app.controllers.user_controllers as user_cnt
import app.controllers.category_controllers as category_cnt
import app.utils.messages as messages 


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", '')
ADMIN_ID = os.getenv("TELEGRAM_ADMIN_ID", '')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
        Sending welcome message to user
    """

    await user_cnt.add_new_user(message.from_user)
    await message.answer(messages.WELCOM_MSG)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
        Sending help message to user
    """
    await message.answer(messages.HELP_MSG)


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """
        Sending category list
    """
    await message.answer(await category_cnt.get_categories_list())


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику трат"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Отправляет статистику трат текущего месяца"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} грн. на {expense.category_name} — нажми "
        f"/del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые траты:\n\n* " + "\n\n* "\
            .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """
        Adding new expense
    """
    try:
        expense = await expense_cnt.add_expense(message.from_user.id, message.text)
    except NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавлены траты {expense['amount']} грн. на {expense['category_name']}.\n\n")
    #    f"{expense_cnt.get_today_statistics()}")
    await message.answer(answer_message)
