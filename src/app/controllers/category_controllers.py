import app.db as db


async def check_db():
    await db.check_db_exists()