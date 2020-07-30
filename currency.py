from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import json
import re


def choose_bank(type, amount, cur_from, cur_to, date):
    if type == 'ЦБ РФ':
        return convert_cbr(amount, cur_from, cur_to, date)
    if type == 'НБ РБ':
        return convert_nbrb(amount, cur_from, cur_to, date)


def convert_cbr(amount, cur_from, cur_to, date):
    response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}')
    soup = BeautifulSoup(response.content, 'xml')
    round_to_2 = Decimal('1.00')
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
    return result.quantize(round_to_2)


def convert_nbrb(amount, cur_from, cur_to, date):
    split_date = re.split('[./]', date)
    corr_date = f'{split_date[2]}-{split_date[1]}-{split_date[0]}'
    response = requests.get(f'https://www.nbrb.by/api/exrates/rates?ondate={corr_date}&periodicity=0')
    soup = BeautifulSoup(response.content, 'lxml').p.next
    data = json.loads(soup)
    round_to_2 = Decimal('1.00')
    round_to_4 = Decimal('1.0000')
    brub = ['BYN', 'BYR']
    curr_list = dict()
    for _ in data:
        curr_list[_['Cur_Abbreviation']] = [Decimal(_['Cur_Scale']), Decimal(_['Cur_OfficialRate']).quantize(round_to_4)]
    if cur_from in brub:
        cur_from_val = Decimal('1')
        cur_from_nom = Decimal('1')
        cur_to_val = curr_list[cur_to][1]
        cur_to_nom = curr_list[cur_to][0]
    elif cur_to in brub:
        cur_to_val = Decimal('1')
        cur_to_nom = Decimal('1')
        cur_from_val = curr_list[cur_from][1]
        cur_from_nom = curr_list[cur_from][0]
    else:
        cur_from_val = curr_list[cur_from][1]
        cur_from_nom = curr_list[cur_from][0]
        cur_to_val = curr_list[cur_to][1]
        cur_to_nom = curr_list[cur_to][0]
    result = (cur_from_val / cur_from_nom) * amount / (cur_to_val / cur_to_nom)
    return result.quantize(round_to_2)


# a = convert_cbr(Decimal('81205.30'), 'USD', 'RUR', '30/06/2020')
# print(a)
# b = convert_cbr(Decimal('1000.1000'), 'RUR', 'JPY', '17/02/2005')
# print(b)
# c = convert_nbrb(Decimal('405979.86'), 'RUB', 'USD', '24/07/2020')
# print(c)  # 5 720.00 USD
