"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from common.printer import print_task


def assert_string_to_bytes(string: str):
    """
    Проверяет может ли строка быть преобразована в байты и выводит информацию в консоль
    :param string: строка для проверки
    """
    try:
        print(f'* Строка "{string}" в байтах: {string.encode("ascii")}\r\n')
    except UnicodeEncodeError:
        print(f'* Строка "{string}" не может быть конвертирована при помощи b"" или с кодировкой ASCII\r\n')


def main():
    print_task(3)
    assert_string_to_bytes('attribute')
    assert_string_to_bytes('класс')
    assert_string_to_bytes('функция')
    assert_string_to_bytes('type')


if __name__ == '__main__':
    main()
