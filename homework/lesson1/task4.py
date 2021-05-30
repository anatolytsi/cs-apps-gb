"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и
выполнить обратное преобразование (используя методы encode и decode).
"""
from homework.common.task_printer import print_task


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
