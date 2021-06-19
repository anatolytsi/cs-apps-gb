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
import argparse
import pickle
from select import select
from socket import *

from log.server_log_config import log_error, log_info, log_critical, log

online_users = []
chats = {}
clients = []


# @log
def send_msg(client: socket, response: dict):
    """
    Шлет ответ клиенту

    :param client: сокет клиента
    :param response: ответ в формате словаря для дальнейшей конвертации в JSON
    """
    client.send(pickle.dumps(response)) if response else None


# @log
def message_authenticate(msg: dict) -> list:
    """
    Обработка сообщения аутентификации

    :param msg: сообщение в формате словаря
    :return: код ответа, тело ответа, флаг ошибки
    """
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
    return [response_code, response_text, response_is_error]


# @log
def message_sent(msg: dict) -> list:
    """
    Обработка пересылки сообщения

    :param msg: сообщение в формате словаря
    :return: код ответа, тело ответа, флаг ошибки
    """
    response_code = 400
    response_text = f'Отправитель или адресат неопределенны'
    response_is_error = True
    if 'from' in msg and msg['from']:
        if 'to' in msg and msg['to']:
            # TODO проверку на существование пользователей
            if msg['to'] in online_users:
                response_code = 200
                response_text = f'Сообщение от {msg["from"]} к {msg["to"]} доставлено'
                response_is_error = False
                for client in clients:
                    send_msg(client, {
                        'response': response_code,
                        'error' if response_is_error else 'alert': response_text
                    })
            else:
                response_code = 400
                response_text = f'Пользователь {msg["to"]} не онлайн'
                response_is_error = True
    return [response_code, response_text, response_is_error]


# @log
def message_join_room(msg: dict) -> list:
    """
    Обработка сообщения присоединения к чату

    :param msg: сообщение в формате словаря
    :return: код ответа, тело ответа, флаг ошибки
    """
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
    return [response_code, response_text, response_is_error]


# @log
def message_leave_room(msg: dict) -> list:
    """
    Обработка сообщения выхода из чата

    :param msg: сообщение в формате словаря
    :return: код ответа, тело ответа, флаг ошибки
    """
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
    return [response_code, response_text, response_is_error]


# @log
def message_quit(msg: dict) -> list:
    """
    Обработка сообщения quit

    :param msg: сообщение в формате словаря
    :return: код ответа, тело ответа, флаг ошибки
    """
    response_code = 200
    response_text = f'Успешно отключен'
    response_is_error = False
    return [response_code, response_text, response_is_error]


# @log
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
        response_code, response_text, response_is_error = message_authenticate(msg)
    else:
        if msg['user']['account_name'] in online_users:
            # TODO убрать заглушки и добавить функционал
            if msg['action'] == 'msg':
                response_code, response_text, response_is_error = message_sent(msg)
            elif msg['action'] == 'presence':
                # TODO keep-alive функцию которая возможно будет обнулять счетчик отсутствия сообщений от клиента
                pass
            elif msg['action'] == 'join':
                response_code, response_text, response_is_error = message_join_room(msg)
            elif msg['action'] == 'leave':
                response_code, response_text, response_is_error = message_leave_room(msg)
            elif msg['action'] == 'quit':
                response_code, response_text, response_is_error = message_quit(msg)
        else:
            response_code = 401
            response_text = f'Пользователь {msg["user"]["account_name"]} не авторизован'
            response_is_error = True

    response = {}
    if response_code:
        if response_is_error:
            log_error(f'{response_code}: {response_text}')
        else:
            log_info(f'{response_code}: {response_text}')
        response = {'response': response_code, 'error' if response_is_error else 'alert': response_text}
    return response


# @log
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
        log_critical(f'Неправильный IP адрес {address}:{port}, проверьте правильность введенного адреса')
        # timed_print(f'Ошибка! Неправильный IP адрес {address}:{port}, проверьте правильность введенного адреса')
        return
    soc.listen(5)
    soc.settimeout(0.2)
    soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    log_info(f'Сервер запущен по адресу {address}:{port}')
    # timed_print(f'Сервер запущен по адресу {address}:{port}')
    return soc


def read_requests_and_get_responses(r_clients, all_clients):
    responses = {}

    for client in r_clients:
        try:
            data = client.recv(1024)
            responses[client] = message_dispatcher(pickle.loads(data))
        except:
            print('Клиент отключился')
            all_clients.remove(client)
    return responses


def write_responses(responses, w_clients, all_clients):
    for client in w_clients:
        if client in responses:
            try:
                send_msg(client, responses[client])
            except:
                print('Клиент отключился')
                all_clients.remove(client)

# @log
def server_listen(soc: socket):
    """
    Основной цикл работы сервера

    :param soc: сокет запущенного сервера
    """
    if not soc:
        return
    while True:
        try:
            client, addr = soc.accept()
            log_info(f'Соединение с клиентом установленно')
            # Соединение с клиентом установленно
        except OSError as e:
            pass
        else:
            clients.append(client)
        finally:
            wait = 5
            r = []
            w = []
            try:
                r, w, e = select(clients, clients, [], wait)
            except:
                # Client disconnected
                pass
            responses = {}
            if r:
                responses = read_requests_and_get_responses(r, clients)
            if w:
                write_responses(responses, w, clients)


# @log
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


# @log
def main():
    args = get_args()
    soc = server_start(args['address'], args['port'])
    server_listen(soc)


if __name__ == '__main__':
    main()

help()
