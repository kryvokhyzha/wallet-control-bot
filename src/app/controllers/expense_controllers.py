import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import app.db as db

from app.Exceptions.NotCorrectMessage import NotCorrectMessage

from app.utils.config import DB_EXPENSES_COLLECTION_NAME

from app.models.category import Categories
from app.models.expense import Expense
from app.models.message import Message


async def add_expense(user_id: int, raw_message: str) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)

    category = Categories()
    await category._init()
    category = category.get_category(parsed_message['category_text'])

    document = { 
        "amount": parsed_message['amount'],
        "created": _get_now_formatted(),
        "category_codename": category['codename'],
        "raw_text": raw_message,
        "user_id": user_id
        }

    inserted_row_id = await db.do_insert_one(DB_EXPENSES_COLLECTION_NAME, document)
    return Expense(user_id=user_id,
                   amount=parsed_message['amount'],
                   category_name=category['name'])


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def get_today_statistics() -> str:
    """Возвращает строкой статистику расходов за сегодня"""
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   "from expense where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]
    cursor.execute("select sum(amount) "
                   "from expense where date(created)=date('now', 'localtime') "
                   "and category_codename in (select codename "
                   "from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    return (f"Расходы сегодня:\n"
            f"всего — {all_today_expenses} грн.\n"
            f"базовые — {base_today_expenses} грн. из {_get_budget_limit()} грн.\n\n"
            f"За текущий месяц: /month")