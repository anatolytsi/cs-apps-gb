"""
Простой клиент на питоне

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
import time
from socket import *

from homework.common.printer import timed_print


def send_data_to_server(server: socket, data: dict) -> bool:
    """
    Отправка данных на сервер

    :param server: присоединенный сервер
    :param data: данные для отправки
    :return: успешность операции
    """
    server.send(pickle.dumps(data))
    # TODO проверку на получение сообщения сервером
    return True


def get_response_from_server(server: socket) -> bool:
    """
    Ожидание ответа от сервера (без таймаута)

    :param server: присоединенный сервер
    :return: успешность операции
    """
    data = server.recv(1024)
    response = pickle.loads(data)
    if 'error' in response:
        timed_print(f'Сервер ответил ошибкой: {response["response"]} {response["error"]}')
        return False
    elif 'alert' in response:
        timed_print(f'Сервер ответил: {response["response"]} {response["alert"]}')
    return True


def authenticate_client(server: socket, username: str, password: str) -> bool:
    """
    Аутентификация клиента
    
    :param server: присоединенный сервер
    :param username: имя пользователя
    :param password: пароль пользователя
    :return: успешность операции
    """
    msg = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": username,
            "password": password
        }
    }
    timed_print(f'Аутентификация {username}...')
    send_data_to_server(server, msg)
    return get_response_from_server(server)


def send_presence(server: socket, username: str) -> bool:
    """
    Отправка presence сообщения
    
    :param server: присоединенный сервер
    :param username: имя аутентифицированного пользователя
    :return: успешность операции
    """
    msg = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": username
        }
    }
    timed_print(f'Шлем presence...')
    return send_data_to_server(server, msg)


def send_msg(server: socket, sender: str, receiver: str, message: str) -> bool:
    """
    Отправить сообщению пользователю/в чат
    
    :param server: присоединенный сервер
    :param sender: имя аутентифицированного пользователя
    :param receiver: получатель/чат
    :param message: сообщение для отправки
    :return: успешность операции
    """
    msg = {
        "action": "msg",
        "time": time.time(),
        "from": sender,
        "to": receiver,
        "message": message,
        "user": {
            "account_name": sender  # Костыль
        }
    }
    timed_print(f'Шлем сообщение от {sender} к {receiver}: {message}')
    send_data_to_server(server, msg)
    return get_response_from_server(server)


def join_room(server: socket, username: str, room: str) -> bool:
    """
    Присоединиться к чату
    
    :param server: присоединенный сервер
    :param username: имя аутентифицированного пользователя
    :param room: имя чата
    :return: успешность операции
    """
    msg = {
        "action": "join",
        "time": time.time(),
        "room": room,
        "user": {
            "account_name": username
        }
    }
    timed_print(f'Пользователь {username} присоединяется к чату {room}...')
    send_data_to_server(server, msg)
    return get_response_from_server(server)


def leave_room(server: socket, username: str, room: str) -> bool:
    """
    Покинуть чат
    
    :param server: присоединенный сервер
    :param username: имя аутентифицированного пользователя
    :param room: имя чата
    :return: успешность операции
    """
    msg = {
        "action": "leave",
        "time": time.time(),
        "room": room,
        "user": {
            "account_name": username
        }
    }
    timed_print(f'Пользователь {username} выходит из чата {room}...')
    send_data_to_server(server, msg)
    return get_response_from_server(server)


def connect_client(address: str, port: int = 7777) -> (socket, None):
    """
    Подключение клиента к серверу
    
    :param address: адрес сервера
    :param port: порт сервера
    :return: возвращает сокет или None если инициализация не прошла
    """
    address = '127.0.0.1' if address == 'localhost' else address
    port = port if port else 7777
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.connect((address, int(port)))
        timed_print(f'Клиент подключился к {address}:{port}')
    except ConnectionRefusedError:
        server = None
        timed_print(f'Ошибка! Сервер {address}:{port} отклонил подключение, проверьте порт или сервер для подключения')
    except TimeoutError:
        server = None
        timed_print(f'Ошибка! Превышено время ожидания ответа от {address}:{port}')
    except gaierror:
        server = None
        timed_print(f'Ошибка! Неправильный IP адрес {address}:{port}, проверьте правильность введенного адреса')
    return server


def disconnect_client(server: socket):
    """
    Отключение клиента от сервера
    
    :param server: подключенный сокет
    """
    server.close()


def get_args() -> dict:
    """
    Получение аргументов для запуска из консоли
    
    :return: словарь с необходимыми аргументами
    """
    parser = argparse.ArgumentParser(description='Простой клиент на Python')
    parser.add_argument('-a', '--address',
                        help='IP адрес сервера',
                        required=True)
    parser.add_argument('-p', '--port',
                        help='Порт сервера, по умолчанию использует 7777',
                        required=False)
    return vars(parser.parse_args())


def main():
    username = 'user'

    args = get_args()

    # По хорошему я бы сделал все это в классе и не нужно было бы каждый раз передавать в метод сервер (сокет)
    server = connect_client(args['address'], args['port'])
    if server:
        authenticate_client(server, username, 'password')
        send_presence(server, username)
        join_room(server, username, '#geekbrains')
        send_msg(server, username, '#geekbrains', 'Всем привет в этом чатике!')
        send_msg(server, username, '#geekbrains', 'Ну и больно надо...')
        leave_room(server, username, '#geekbrains')
        disconnect_client(server)


if __name__ == '__main__':
    main()
