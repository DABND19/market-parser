import asyncio
from csv import DictWriter
from datetime import datetime
from io import StringIO

import aiohttp
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import Session
from db.models.product import Product, Market
from db.selectors.product import select_products, select_report
from loader import dp
from parsers import wildberries
from utils.with_scraper import with_scraper_api


PARSERS = {Market.WILDBERRIES: wildberries.parse_content}


async def fetch_html(product: Product, session: aiohttp.ClientSession) -> bytes:
    request_url = with_scraper_api(product.original_url)

    async with session.get(request_url) as response:
        if not response:
            return None
        return await response.text()


async def update_prices(session: AsyncSession):
    products = await select_products(session)

    async with aiohttp.ClientSession() as client_session:
        tasks_to_fetch = [asyncio.create_task(fetch_html(product, client_session)) for product in products]
        contents = await asyncio.gather(*tasks_to_fetch)

    for product, content in zip(products, contents):
        if not content:
            continue

        parser = PARSERS.get(product.market)
        if not parser:
            continue

        parsed_data = parser(content)
        product.price = parsed_data['price']

        product.updated_at_dt = datetime.now()

    await session.commit()


async def prepare_report(session: AsyncSession) -> StringIO:
    records = await select_report(session)
    buffer = StringIO()
    
    field_names = ['Наименование товара', 'Конкурент',
                   'Ссылка конкурента', 'Цена конкурента', 
                   'Цена', 'Ссылка']
    writer = DictWriter(buffer, fieldnames=field_names)
    writer.writeheader()

    for record in records:
        competitor_id, product_name, competitor_url, competitor_price, competitor_name, \
           product_id, product_url, product_price = record
        obj = {'Наименование товара': product_name, 
               'Конкурент': competitor_name,
               'Ссылка конкурента': competitor_url, 
               'Цена конкурента': competitor_price, 
               'Ссылка': product_url, 
               'Цена': product_price}
        writer.writerow(obj)

    buffer.seek(0)
    return buffer


@dp.message_handler(Command('get_report'))
async def get_report(message: Message):
    async with Session() as db_session:
        placeholder = await message.answer(f'Обновление цен на товары...')

        await update_prices(db_session)

        await placeholder.edit_text(f'Формирование файла отчета...')

        report_file = await prepare_report(db_session)
        report_file.name = 'Отчет.csv'
        await placeholder.delete()
        await message.answer_document(report_file, caption='Данные о ценах обновлены')
