from typing import Dict
import app.db as db


async def add_new_user(documnet: Dict):
    is_register = await db.user_is_exists(documnet['id'])

    if is_register:
        await db.do_update(documnet)
    else:
        await db.do_insert(documnet)
