from bs4 import BeautifulSoup
from decimal import Decimal
import requests


# TODO добавить в функцию в качестве последнего параметра requests
# response = requests.get()  # Использовать переданный requests
def convert(amount, cur_from, cur_to, date):
    response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}')
    soup = BeautifulSoup(response.content, 'xml')
    round_to_4 = Decimal('1.0000')
    rub = ['RUR', 'RUB']
    if cur_from in rub:
        cur_from_val = Decimal('1')
        cur_from_nom = Decimal('1')
        cur_to_val = Decimal(soup.find('CharCode', text=cur_to).find_next_sibling('Value').string.replace(',', '.'))
        cur_to_nom = Decimal(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string.replace(',', '.'))
    elif cur_to in rub:
        cur_to_val = Decimal('1')
        cur_to_nom = Decimal('1')
        cur_from_val = Decimal(soup.find('CharCode', text=cur_from).find_next_sibling('Value').string.replace(',', '.'))
        cur_from_nom = Decimal(soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string.replace(',', '.'))
    else:
        cur_from_val = Decimal(soup.find('CharCode', text=cur_from).find_next_sibling('Value').string.replace(',', '.'))
        cur_from_nom = Decimal(soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string.replace(',', '.'))
        cur_to_val = Decimal(soup.find('CharCode', text=cur_to).find_next_sibling('Value').string.replace(',', '.'))
        cur_to_nom = Decimal(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string.replace(',', '.'))
    result = (cur_from_val / cur_from_nom) * amount / (cur_to_val / cur_to_nom)
    return result.quantize(round_to_4)


a = convert(Decimal('81205.30'), 'USD', 'RUR', '30/06/2020')
print(a)
b = convert(Decimal('1000.1000'), 'RUR', 'JPY', '17/02/2005')
print(b)
