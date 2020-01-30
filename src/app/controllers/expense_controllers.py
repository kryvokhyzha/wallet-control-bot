import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import app.db as db

from app.exceptions.NotCorrectMessage import NotCorrectMessage

from app.utils.config import DB_EXPENSES_COLLECTION_NAME, DB_CATEGORY_COLLECTION_NAME, DB_USER_COLLECTION_NAME

from app.models.category import Categories
from app.models.expense import Expense
from app.models.message import Message

from bson.objectid import ObjectId


async def add_expense(user_id: int, raw_message: str) -> Expense:
    """
        Adding new expense
    """
    parsed_message = _parse_message(raw_message)

    category = Categories()
    await category._init()
    category = category.get_category(parsed_message['category_text'])

    document = { 
        "amount": parsed_message['amount'],
        "created": _get_now_datetime(),
        "category_codename": category['codename'],
        "is_base_expense": category['is_base_expense'],
        "user_id": user_id
        }

    inserted_row_id = await db.do_insert_one(DB_EXPENSES_COLLECTION_NAME, document)
    return Expense(user_id=user_id,
                   amount=parsed_message['amount'],
                   category_name=category['name'])


def _parse_message(raw_message: str) -> Message:
    """
        Parsing text message about new expense
    """
    regexp_result = re.match(r"[+]?([0-9]*\.[0-9]+|[0-9]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро")

    amount = float(regexp_result.group(1).replace(" ", ""))
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    """
        Return current date
    """
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """
        Return current date with time zone
    """
    tz = pytz.timezone("Europe/Kiev")
    now = datetime.datetime.now(tz)
    return now


async def get_today_statistics(user_id: int) -> str:
    """
        Return statistics for current date
    """

    now = _get_now_datetime()
    start = _get_now_datetime().replace(hour=0, minute=0, second=0, microsecond=0)

    document = {'user_id': user_id, 'created': {'$lt': now, '$gte': start}}

    result = await db.compute_sum(DB_EXPENSES_COLLECTION_NAME, 'amount', document)

    if not result:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result

    document = {'user_id': user_id, 'is_base_expense': True, 'created': {'$lt': now, '$gte': start}}

    result = await db.compute_sum(DB_EXPENSES_COLLECTION_NAME, 'amount', document)

    base_today_expenses = result if result else 0
    return (f"Расходы сегодня:\n"
            f"всего — {round(all_today_expenses, 2)} грн.\n"
            f"базовые — {round(base_today_expenses, 2)} грн. из {await _get_budget_limit(user_id)} грн.\n\n"
            f"За текущий месяц: /month")


async def get_month_statistics(user_id: int) -> str:
    """
        Return statistics for current month
    """
    now = _get_now_datetime()
    start = _get_now_datetime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    document = {'user_id': user_id, 'created': {'$lt': now, '$gte': start}}

    result = await db.compute_sum(DB_EXPENSES_COLLECTION_NAME, 'amount', document)

    if not result:
        return "В этом месяце ещё нет расходов"
    all_today_expenses = result
    
    document = {'user_id': user_id, 'is_base_expense': True, 'created': {'$lt': now, '$gte': start}}

    result = await db.compute_sum(DB_EXPENSES_COLLECTION_NAME, 'amount', document)

    budget = await _get_budget_limit(user_id)

    base_today_expenses = result if result else 0
    return (f"Расходы в текущем месяце:\n"
            f"всего — {round(all_today_expenses, 2)} грн.\n"
            f"базовые — {round(base_today_expenses, 2)} грн. из "
            f"{now.day * budget} грн.")


async def last(user_id: int) -> List[Expense]:
    """
        Return few last expenses
    """

    rows = await db.do_find(DB_EXPENSES_COLLECTION_NAME, {'user_id': user_id}, sort_param={'sort_by': 'created', 'sort_type': -1}, limit=5)

    last_expenses = []
    for row in rows:
        category_name = await db.do_find_one(DB_CATEGORY_COLLECTION_NAME, {'codename': row['category_codename']})
        last_expenses.append(Expense(id=row['_id'], amount=row['amount'], category_name=category_name['name']))
    
    return last_expenses


async def delete_expense(row_id: str) -> None:
    """
        Delete message my _id
    """
    await db.do_delete_one(DB_EXPENSES_COLLECTION_NAME, {'_id': ObjectId(row_id)})


async def _get_budget_limit(user_id) -> int:
    """
        Changing daily limit for base expense
    """
    user = await db.do_find_one(DB_USER_COLLECTION_NAME, {'id': user_id})
    return user['budget']
