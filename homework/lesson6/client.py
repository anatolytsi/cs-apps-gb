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

from log.client_log_config import log_info, log_error, log_critical, log


@log
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


@log
def get_response_from_server(server: socket, test_response: dict = None) -> bool:
    """
    Ожидание ответа от сервера (без таймаута)

    :param server: присоединенный сервер
    :param test_response: тестовый ответ от сервера
    :return: успешность операции
    """
    if test_response:
        response = test_response
    else:
        data = server.recv(1024)
        response = pickle.loads(data)
    if 'error' in response:
        log_error(f'Сервер ответил ошибкой: {response["response"]} {response["error"]}')
        return False
    elif 'alert' in response:
        log_info(f'Сервер ответил: {response["response"]} {response["alert"]}')
    return True


@log
def authenticate_client(server: socket, username: str, password: str, test_response: dict = None) -> bool:
    """
    Аутентификация клиента
    
    :param server: присоединенный сервер
    :param username: имя пользователя
    :param password: пароль пользователя
    :param test_response: тестовый ответ от сервера
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
    log_info(f'Аутентификация {username}...')
    send_data_to_server(server, msg) if not test_response else None
    return get_response_from_server(server, test_response)


@log
def send_presence(server: socket, username: str, test_response: dict = None) -> bool:
    """
    Отправка presence сообщения
    
    :param server: присоединенный сервер
    :param username: имя аутентифицированного пользователя
    :param test_response: тестовый ответ от сервера
    :return: успешность операции
    """
    msg = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": username
        }
    }
    log_info(f'Шлем presence...')
    return send_data_to_server(server, msg) if not test_response else True


@log
def send_msg(server: socket, sender: str, receiver: str, message: str, test_response: dict = None) -> bool:
    """
    Отправить сообщению пользователю/в чат
    
    :param server: присоединенный сервер
    :param sender: имя аутентифицированного пользователя
    :param receiver: получатель/чат
    :param message: сообщение для отправки
    :param test_response: тестовый ответ от сервера
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
    log_info(f'Шлем сообщение от {sender} к {receiver}: {message}')
    send_data_to_server(server, msg) if not test_response else None
    return get_response_from_server(server, test_response)


@log
def join_room(server: socket, username: str, room: str, test_response: dict = None) -> bool:
    """
    Присоединиться к чату
    
    :param server: присоединенный сервер
    :param username: имя аутентифицированного пользователя
    :param room: имя чата
    :param test_response: тестовый ответ от сервера
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
    log_info(f'Пользователь {username} присоединяется к чату {room}...')
    send_data_to_server(server, msg) if not test_response else None
    return get_response_from_server(server, test_response)


@log
def leave_room(server: socket, username: str, room: str, test_response: dict = None) -> bool:
    """
    Покинуть чат
    
    :param server: присоединенный сервер
    :param username: имя аутентифицированного пользователя
    :param room: имя чата
    :param test_response: тестовый ответ от сервера
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
    log_info(f'Пользователь {username} выходит из чата {room}...')
    send_data_to_server(server, msg) if not test_response else None
    return get_response_from_server(server, test_response)


@log
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
        log_info(f'Клиент подключился к {address}:{port}')
    except ConnectionRefusedError:
        server = None
        log_critical(f'Ошибка! Сервер {address}:{port} отклонил подключение, проверьте порт или сервер для подключения')
    except TimeoutError:
        server = None
        log_critical(f'Ошибка! Превышено время ожидания ответа от {address}:{port}')
    except gaierror:
        server = None
        log_critical(f'Ошибка! Неправильный IP адрес {address}:{port}, проверьте правильность введенного адреса')
    return server


@log
def disconnect_client(server: socket):
    """
    Отключение клиента от сервера
    
    :param server: подключенный сокет
    """
    server.close()


@log
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


@log
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
