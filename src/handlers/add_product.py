import json

from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from sqlalchemy.exc import IntegrityError

from db.engine import Session
from db.models.product import Market, Product
from loader import dp


class ProductForm(StatesGroup):
    market = State()
    name = State()
    original_url = State()
    competitor_urls = State()


MARKET_LIST = [market.value for market in Market]


@dp.message_handler(Command('add_product'), state=None)
async def add_product(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for market in Market:
        keyboard.add(market.value)

    await message.answer('Выберите торговую площадку: ', reply_markup=keyboard)
    await ProductForm.market.set()

@dp.message_handler(lambda msg: not msg.text in MARKET_LIST, state=ProductForm.market)
async def process_invalid_market_name(message: Message, state: FSMContext):
    await message.answer(f'Такая торговая площадка не поддерживается. Доступны: {", ".join(MARKET_LIST)}.')

@dp.message_handler(lambda msg: msg.text in MARKET_LIST, state=ProductForm.market)
async def set_product_market(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['market'] = message.text

    keyboard = ReplyKeyboardRemove()

    await message.answer('Введите название товара: ', reply_markup=keyboard)
    await ProductForm.name.set()

@dp.message_handler(state=ProductForm.name)
async def set_product_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Вставьте ссылку на товар: ')
    await ProductForm.original_url.set()

@dp.message_handler(state=ProductForm.original_url)
async def set_product_original_url(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['original_url'] = message.text

    await message.answer('Вставьте ссылки на товары конкурентов: ')
    await ProductForm.competitor_urls.set()

@dp.message_handler(state=ProductForm.competitor_urls)
async def set_product_competitor_urls(message: Message, state: FSMContext):
    async with state.proxy() as data, Session() as db_session:
        data['competitor_urls'] = message.text.split('\n')

        main_product = Product(name=data['name'], original_url=data['original_url'], market=data['market'])
        db_session.add(main_product)
        await db_session.commit()
        
        competitor_products = [Product(name=data['name'], 
                                       original_url=url,
                                       market=data['market'], 
                                       competitor_id=main_product.id) for url in data['competitor_urls']]
        db_session.add_all(competitor_products)
        await db_session.commit()

    await state.finish()
    await message.answer('Товар добавлен')
