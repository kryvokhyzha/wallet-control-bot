from aiogram import executor
from app.bot import dp
from app.db import check_db_exists


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=check_db_exists)
