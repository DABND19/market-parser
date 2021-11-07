import re

from bs4 import BeautifulSoup


def parse_content(raw_data: bytes) -> dict:
    html = BeautifulSoup(raw_data, 'html.parser')

    info_block = html.body.find(id='infoBlockProductCard')

    price_block = info_block.find('div', attrs={'class': 'price-block'})
    price = price_block.find('span', attrs={'class': 'price-block__commission-current-price'})

    return dict(price=re.sub(r'[^0-9.,]', '', price.text))
