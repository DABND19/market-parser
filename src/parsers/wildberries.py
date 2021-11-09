import logging
import re
from typing import Optional

from bs4 import BeautifulSoup


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def parse_content(raw_data: bytes) -> Optional[dict]:
    html = BeautifulSoup(raw_data, 'html.parser')

    info_block = html.find(id='infoBlockProductCard')
    if not info_block:
        logger.error('Can\'t find info block.')
        return None

    price_block = info_block.find('div', attrs={'class': 'price-block'})
    price = price_block.find('span', attrs={'class': 'price-block__commission-current-price'})
    if not price: 
        logger.error('Can\'t parse price.')
        return None

    return dict(price=re.sub(r'[^0-9.,]', '', price.text))
