from aiogram import executor
from app.bot import dp
from app.bot import on_startup, on_shutdown

from app.utils.config import HOST, PORT, WEBHOOK_PATH, DEVELOP


if __name__ == '__main__':
    if DEVELOP == 'False':
        executor.start_webhook(dispatcher=dp,
                               skip_updates=True,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               webhook_path=WEBHOOK_PATH,
                               host=HOST,
                               port=PORT)
    else:     
        executor.start_polling(dispatcher=dp,
                               skip_updates=True,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown)
        
