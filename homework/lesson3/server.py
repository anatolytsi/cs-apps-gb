"""
Простой сервер на питоне

Функции клиента:
* сформировать presence-сообщение;
* отправить сообщение серверу;
* получить ответ сервера;
* разобрать сообщение сервера;
* параметры командной строки скрипта `client.py <addr> [<port>]`:
    - addr — ip-адрес сервера;
    - port — tcp-порт на сервере, по умолчанию 7777.
"""
import os
import sys
import argparse
import pickle
import time
from socket import *

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from homework.common.printer import timed_print

online_users = []
chats = {}


def send_msg(client: socket, response: dict):
    """
    Шлет ответ клиенту

    :param client: сокет клиента
    :param response: ответ в формате словаря для дальнейшей конвертации в JSON
    """
    client.send(pickle.dumps(response)) if response else None


def message_dispatcher(msg: dict) -> dict:
    """
    Распаковщик сообщений от клиентов

    :param msg: сообщение в формате словаря
    :return: ответ в формате словаря
    """
    # Решение сделать переменные вместо структур было принято для нормального вывода в консоль
    response_code = None
    response_text = None
    response_is_error = None
    if msg['action'] == 'authenticate':
        # Если запросил аутентификацию
        if msg['user']['account_name'] not in online_users:
            # Если пользователь не аутентифицирован
            # TODO нормальную проверку пароля
            if msg['user']['password'] == 'password':
                # Если пароль совпадает с соответсвующим паролем (в нормальной ситуации у каждого пользователя свой
                # пароль, естественно)
                online_users.append(msg['user']['account_name'])
                response_code = 202
                response_text = f'Пользователь {msg["user"]["account_name"]} аутентифицирован'
                response_is_error = False
            else:
                response_code = 402
                response_text = f'Пользователь {msg["user"]["account_name"]} не существует или введен неправильный ' \
                                f'пароль '
                response_is_error = True
        else:
            response_code = 200
            response_text = f'Пользователь {msg["user"]["account_name"]} уже аутентифицирован'
            response_is_error = False
    else:
        if msg['user']['account_name'] in online_users:
            # TODO убрать заглушки и добавить функционал
            if msg['action'] == 'msg':
                response_code = 400
                response_text = f'Отправитель или адресат неопределенны'
                response_is_error = True
                if 'from' in msg:
                    if 'to' in msg:
                        # TODO проверку на существование пользователей
                        response_code = 200
                        response_text = f'Сообщение от {msg["from"]} к {msg["to"]} доставлено'
                        response_is_error = False
            elif msg['action'] == 'presence':
                # TODO keep-alive функцию которая возможно будет обнулять счетчик отсутствия сообщений от клиента
                pass
            elif msg['action'] == 'join':
                if 'room' in msg:
                    # TODO сделать комнаты и присоединения к ним
                    if msg["room"] not in chats:
                        chats[msg["room"]] = []
                    chats[msg["room"]].append(msg["user"]["account_name"])
                    response_code = 200
                    response_text = f'Пользователь {msg["user"]["account_name"]} присоединился к чату {msg["room"]}'
                    response_is_error = False
                else:
                    response_code = 400
                    response_text = f'Не указан чат для присоединения'
                    response_is_error = True
            elif msg['action'] == 'leave':
                if 'room' in msg:
                    if msg["room"] in chats:
                        if msg["user"]["account_name"] in chats[msg["room"]]:
                            chats[msg["room"]].remove(msg["user"]["account_name"])
                            response_code = 200
                            response_text = f'Пользователь {msg["user"]["account_name"]} покинул чат {msg["room"]}'
                            response_is_error = False
                        else:
                            response_code = 403
                            response_text = f'Пользователь {msg["user"]["account_name"]} не состоит в чате ' \
                                            f'{msg["room"]}'
                            response_is_error = True
                    else:
                        response_code = 400
                        response_text = f'Чата {msg["room"]} не существует'
                        response_is_error = True
                else:
                    response_code = 400
                    response_text = f'Неуказанна комната для присоединения'
                    response_is_error = True
            elif msg['action'] == 'quit':
                response_code = 200
                response_text = f'Успешно отключен'
                response_is_error = False
        else:
            response_code = 401
            response_text = f'Пользователь {msg["user"]["account_name"]} не авторизован'
            response_is_error = True

    response = {}
    if response_code:
        print(
            f'[{time.strftime("%H:%M:%S")}] Сервер отвечает: {response_code} '
            f'{"Ошибка! " if response_is_error else ""}{response_text}')
        response = {'response': response_code, 'error' if response_is_error else 'alert': response_text}
    return response


def server_start(address: str = '', port: int = 7777) -> (socket, None):
    """
    Запускает сервер по заданному адресу и порту

    :param address: адрес запускаемого сервера
    :param port: порт запускаемого сервера
    :return: возвращает сокет или None если инициализация не прошла
    """
    address = '127.0.0.1' if address == 'localhost' else address if address else ''
    port = port if port else 7777
    soc = socket(AF_INET, SOCK_STREAM)
    try:
        soc.bind((address, int(port)))
    except gaierror:
        timed_print(f'Ошибка! Неправильный IP адрес {address}:{port}, проверьте правильность введенного адреса')
        return
    soc.listen(5)
    soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    timed_print(f'Сервер запущен по адресу {address}:{port}')
    return soc


def server_listen(soc: socket):
    """
    Основной цикл работы сервера

    :param soc: сокет запущенного сервера
    """
    if not soc:
        return
    while True:
        client, addr = soc.accept()
        # Соединение с клиентом установленно
        while True:
            # Получаем данные пока клиент подключен и что то шлет
            try:
                data = client.recv(1024)
                response = message_dispatcher(pickle.loads(data))
                send_msg(client, response)
            except (ConnectionResetError, EOFError):
                # Клиент вышел сам
                break
        client.close()


def get_args() -> dict:
    """
    Получение аргументов для запуска из консоли

    :return: словарь с необходимыми аргументами
    """
    parser = argparse.ArgumentParser(description='Простой сервер на Python')
    parser.add_argument('-a', '--address',
                        help='IP адрес сервера, по умолчанию слушает все доступные адреса',
                        required=False)
    parser.add_argument('-p', '--port',
                        help='Порт сервера, по умолчанию использует 7777',
                        required=False)
    return vars(parser.parse_args())


def main():
    args = get_args()
    soc = server_start(args['address'], args['port'])
    server_listen(soc)


if __name__ == '__main__':
    main()
