"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""


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
    print(f'{"=" * 69}\r\n{"=" * 29} Задание 3 {"=" * 29}\r\n{"=" * 69}\r\n')
    assert_string_to_bytes('attribute')
    assert_string_to_bytes('класс')
    assert_string_to_bytes('функция')
    assert_string_to_bytes('type')


if __name__ == '__main__':
    main()
