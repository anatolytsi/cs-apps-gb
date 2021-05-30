"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать скрипт,
автоматизирующий его заполнение данными. Для этого:

a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена
(price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;

b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json
import time

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
    with open(ORDERS_JSON) as f:
        data = json.load(f)
        data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    with open(ORDERS_JSON, 'w') as f:
        f.write(json.dumps(data, indent=4))


def main():
    print(f'{"=" * 69}\r\n{"=" * 29} Задание 2 {"=" * 29}\r\n{"=" * 69}\r\n')
    write_order_to_json('Пальто', 1, 20000, 'Человек Человекович', time.time())


if __name__ == '__main__':
    main()
