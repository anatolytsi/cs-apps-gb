"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт,
автоматизирующий его заполнение данными. Для этого:

a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена
(price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;

b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import os
import sys
import json
import time

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from homework.common.printer import print_task

CURRENT_DIR = os.path.dirname(__file__)

ORDERS_JSON = 'orders.json'


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: float):
    """
    Добавляет определенный товар в заказы (в JSON)

    :param item: название товара
    :param quantity: количество товара
    :param price: цена товара
    :param buyer: покупатель
    :param date: время заказа
    """
    data = []
    filepath = f'{CURRENT_DIR}\\{ORDERS_JSON}'
    with open(filepath) as f:
        data = json.load(f)
        data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=4))


def main():
    print_task(2)
    write_order_to_json('Пальто', 1, 20000, 'Человек Человекович', time.time())


if __name__ == '__main__':
    main()
