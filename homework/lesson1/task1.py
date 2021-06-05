"""
Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и
также проверить тип и содержимое переменных.
"""
from homework.common.task_printer import print_task


def compare_string_with_unicode(string_format: str, unicode_format: str):
    """
    Вывод в консоль информации о значениях и типах переменных строки и юникода
    :param string_format: строковое значение
    :param unicode_format: значение в символьном формате юникод из онлайн конвертера
    """
    print(f'* Строка "{string_format}":\r\n'
          f'\t- cтроковое значение: "{string_format}", тип: {type(string_format)}, длина: {len(string_format)}\r\n'
          f'\t- unicode: "{unicode_format}", тип: "{type(unicode_format)}", длина: {len(unicode_format)}\r\n'
          f'\t- они {"не " if string_format != unicode_format else ""}идентичны друг другу!\r\n'
          )


def main():
    print_task(1)
    compare_string_with_unicode('разработка', '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430')
    compare_string_with_unicode('сокет', '\u0441\u043e\u043a\u0435\u0442')
    compare_string_with_unicode('декоратор', '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440')


if __name__ == '__main__':
    main()
