from typing import Dict
from aiogram import types

from app.models.user import User

from app.utils.config import DB_USER_COLLECTION_NAME

import app.db as db


async def add_new_user(user: types.User):
    new_user = User(id=user.id,
                    username=user.username,
                    is_bot=user.is_bot,
                    language_code=user.language_code)

    is_register = await user_is_exists(new_user['id'])

    if is_register:
        await db.do_update(DB_USER_COLLECTION_NAME, new_user)
    else:
        await db.do_insert_one(DB_USER_COLLECTION_NAME, new_user)


async def user_is_exists(id: int) -> bool:
    if await db.do_find_one(DB_USER_COLLECTION_NAME, {'id': id}):
        return True
    else:
        return False
