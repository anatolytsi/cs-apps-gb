"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from common.printer import print_task


def write_to_file(filename: str, data: list):
    """
    Создает/перезаписывает в указанный файл переданные данные, выводит кодировку файла
    :param filename: имя файла
    :param data: список данных
    """
    print(f'* Пишем в файл {filename}...')
    with open(filename, 'w') as file:
        for line in data:
            file.write(line)
        print(f'\t- Кодировка записанного файла: {file.encoding}\r\n')


def read_file_in_utf8(filename: str):
    """
    Считывает данные из файла и выводит в консоль кодировку с которой был открыт файл и данные в нем
    :param filename: имя файла
    """
    data = []
    print(f'* Читаем файл {filename}...')
    try:
        with open(filename, encoding='utf-8', errors='replace') as file:
            print(f'\t- Кодировка открытого файла: {file.encoding}')
            for line in file:
                data.append(line)
        print(f'\t- Данные считанные из файле: {data}\r\n')
    except UnicodeDecodeError:
        print('\t- Ошибка декодирования данных!\r\n')


def main():
    print_task(6)
    write_to_file('test_file.txt', ['сетевое программирование', 'сокет', 'декоратор'])
    read_file_in_utf8('test_file.txt')


if __name__ == '__main__':
    main()
