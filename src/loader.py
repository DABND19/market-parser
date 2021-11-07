from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import BOT_TOKEN


bot = Bot(BOT_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)
