from aiogram import executor

from db import engine
from db.models import Base
import handlers
from loader import dp


async def on_startup(*args):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
