"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
кириллице.
"""
import subprocess
import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from common.printer import print_task


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
    print_task(5)
    ping_website('yandex.ru')
    ping_website('youtube.com')


if __name__ == '__main__':
    main()
