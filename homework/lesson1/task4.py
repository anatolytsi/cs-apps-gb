"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и
выполнить обратное преобразование (используя методы encode и decode).
"""
import os
import sys

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from homework.common.printer import print_task


def encode_decode_string(string: str):
    """
    Кодирует и декодирует введенную строку и выводит информацию в консоль
    :param string: строка для теста
    """
    encoded = string.encode()
    decoded = encoded.decode()
    print(f'* Строка "{string}":\r\n\t- в закодированном виде: {encoded}\r\n\t- после декодинга: "{decoded}"\r\n')


def main():
    print_task(4)
    encode_decode_string('разработка')
    encode_decode_string('администрирование')
    encode_decode_string('protocol')
    encode_decode_string('standard')


if __name__ == '__main__':
    main()
