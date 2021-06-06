"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
Для этого:

a. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке
ASCII (например, €);

b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;

c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
import os
import sys
import json
import yaml

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from homework.common.printer import print_task

CURRENT_DIR = os.path.dirname(__file__)

ORDERS_JSON = 'orders.json'


def get_data() -> dict:
    """
    Читает JSON-файл с заказами и выдает данные

    :return: словарь данных
    """
    filepath = f'{CURRENT_DIR}\\{ORDERS_JSON}'
    with open(filepath) as f:
        return json.load(f)


def save_and_verify(filename: str, data: dict = None):
    """
    Сохраняет принятые данные в указанный yaml документ в папке скрипта

    :param filename: имя или путь к файлу в папке скрипта
    :param data: словарь данных
    """
    filepath = f'{CURRENT_DIR}\\{filename if ".yaml" in filename else f"{filename}.yaml"}'

    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    print(f'* Прочитанный файл {filepath}:\r\n')
    with open(filepath) as f:
        print(f.read())


def main():
    print_task(3)
    save_and_verify('file', get_data())


if __name__ == '__main__':
    main()
