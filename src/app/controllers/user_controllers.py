import re

from typing import Dict
from aiogram import types

from app.models.user import User

from app.utils.config import DB_USER_COLLECTION_NAME
from app.utils.constants import DEFAULT_BUDGET

import app.db as db


async def add_new_user(user: types.User):
    new_user = User(id=user.id,
                    username=user.username,
                    is_bot=user.is_bot,
                    language_code=user.language_code,
                    budget=DEFAULT_BUDGET)

    is_register = await user_is_exists(new_user['id'])

    if is_register:
        await db.do_replace_one(DB_USER_COLLECTION_NAME, new_user)
    else:
        await db.do_insert_one(DB_USER_COLLECTION_NAME, new_user)


async def user_is_exists(id: int) -> bool:
    if await db.do_find_one(DB_USER_COLLECTION_NAME, {'id': id}):
        return True
    else:
        return False


async def set_budget(user_id: int, raw_message: str) -> float:
    budget = _parse_message(raw_message)
    
    document = {'id': user_id}
    set_document = {'$set': {'budget': budget}}

    await db.do_update_one(DB_USER_COLLECTION_NAME, document, set_document)

    return budget


def _parse_message(raw_message: str) -> float:
    regexp_result = re.match(r"(/.*) [+]?([0-9]*\.[0-9]+|[0-9]+)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n/set_budget 1500")

    return float(regexp_result.group(2).strip())