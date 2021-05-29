"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
кириллице.
"""
import subprocess


def ping_website(url: str):
    """
    Пингует выбранный сайт и выводит информацию в консоль
    :param url: сайт для пинга
    """
    subproc_ping = subprocess.Popen(['ping', url], stdout=subprocess.PIPE)
    print(f'* Сайт {url}:')
    for line in subproc_ping.stdout:
        decoded = line.decode('utf-8').replace('\r\n', '')
        print(f'\t- {decoded}') if decoded else ''
    print('\r\n')


def main():
    print(f'{"=" * 69}\r\n{"=" * 29} Задание 5 {"=" * 29}\r\n{"=" * 69}\r\n')
    ping_website('yandex.ru')
    ping_website('youtube.com')


if __name__ == '__main__':
    main()
