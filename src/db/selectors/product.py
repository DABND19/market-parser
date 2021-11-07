from typing import List, Tuple

from sqlalchemy.sql import select, alias
from sqlalchemy.ext.asyncio import AsyncSession

from db import Session
from db.models import Product


async def select_products(session: AsyncSession) -> List[Product]:
    statement = select(Product)
    result = await session.execute(statement)
    return result.scalars().all()


async def select_report(session: AsyncSession) -> List[Tuple]:
    substatement = select(Product).where(Product.competitor_id != None).cte()
    statement = select(substatement.c.id, substatement.c.name, substatement.c.original_url, substatement.c.price, 
                       Product.id, Product.original_url, Product.price)\
        .join(Product, substatement.c.competitor_id == Product.id)
    result = await session.execute(statement)
    return result.all()
