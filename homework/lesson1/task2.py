"""
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""


def print_string_bytes_info(string: str):
    """
    Вывод в консоль информации о строке в байтовом формате
    :param string: исходная строка
    :return:
    """
    string_bytes = bytes(string, 'raw_unicode_escape')
    print(f'{"*" * 69}\r\n'
          f'* Строковое значение: "{string}"\r\n'
          f'* В байтах: {string_bytes}, тип: "{type(string_bytes)}", длина: {len(string_bytes)}\r\n'
          f'{"*" * 69}\r\n')


def main():
    print(f'{"=" * 69}\r\n{"=" * 29} Задание 2 {"=" * 29}\r\n{"=" * 69}\r\n')
    print_string_bytes_info('class')
    print_string_bytes_info('function')
    print_string_bytes_info('method')


if __name__ == '__main__':
    main()
