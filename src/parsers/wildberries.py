import re
from typing import Optional

from bs4 import BeautifulSoup


def parse_content(raw_data: bytes) -> Optional[dict]:
    html = BeautifulSoup(raw_data, 'html.parser')

    info_block = html.body.find(id='infoBlockProductCard')
    if not info_block:
        return None

    price_block = info_block.find('div', attrs={'class': 'price-block'})
    price = price_block.find('span', attrs={'class': 'price-block__commission-current-price'})

    return dict(price=re.sub(r'[^0-9.,]', '', price.text))
