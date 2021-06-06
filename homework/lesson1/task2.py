"""
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""
from homework.common.printer import print_task


def print_string_bytes_info(string: str):
    """
    Вывод в консоль информации о строке в байтовом формате
    :param string: исходная строка
    :return:
    """
    string_bytes = bytes(string, 'raw_unicode_escape')
    print(f'* Строка "{string}"\r\n'
          f'\t- в байтах: {string_bytes}\r\n\t- тип: {type(string_bytes)}\r\n\t- длина: {len(string_bytes)}\r\n')


def main():
    print_task(2)
    print_string_bytes_info('class')
    print_string_bytes_info('function')
    print_string_bytes_info('method')


if __name__ == '__main__':
    main()
