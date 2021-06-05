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


def get_response_from_server(server: socket):
    data = server.recv(1024)
    response = pickle.loads(data)
    if 'error' in response:
        print(f'[{time.strftime("%H:%M:%S")}] Сервер ответил ошибкой: {response["response"]} {response["error"]}')
    elif 'alert' in response:
        print(f'[{time.strftime("%H:%M:%S")}] Сервер ответил: {response["response"]} {response["alert"]}')


def authenticate_client(server: socket, username: str, password: str):
    msg = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": username,
            "password": password
        }
    }
    print(f'[{time.strftime("%H:%M:%S")}] Аутентификация {username}...')
    server.send(pickle.dumps(msg))
    get_response_from_server(server)


def send_presence(server: socket, username: str):
    msg = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": username
        }
    }
    print(f'[{time.strftime("%H:%M:%S")}] Шлем presence...')
    server.send(pickle.dumps(msg))


def send_msg(server: socket, sender: str, receiver: str, message: str):
    msg = {
        "action": "msg",
        "time": time.time(),
        "from": sender,
        "to": receiver,
        "message": message,
        "user": {
            "account_name": sender
        }
    }
    print(f'[{time.strftime("%H:%M:%S")}] Шлем сообщение от {sender} к {receiver}: {message}')
    server.send(pickle.dumps(msg))
    get_response_from_server(server)


def join_room(server: socket, username: str, room: str):
    msg = {
        "action": "join",
        "time": time.time(),
        "room": room,
        "user": {
            "account_name": username
        }
    }
    print(f'[{time.strftime("%H:%M:%S")}] Пользователь {username} присоединяется к чату {room}...')
    server.send(pickle.dumps(msg))
    get_response_from_server(server)


def leave_room(server: socket, username: str, room: str):
    msg = {
        "action": "leave",
        "time": time.time(),
        "room": room,
        "user": {
            "account_name": username
        }
    }
    print(f'[{time.strftime("%H:%M:%S")}] Пользователь {username} выходит из чата {room}...')
    server.send(pickle.dumps(msg))
    get_response_from_server(server)


def connect_client(addr: str, port: int = 7777) -> socket:
    port = port if port else 7777
    addr = '127.0.0.1' if addr == 'localhost' else addr
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.connect((addr, int(port)))
        print(f'[{time.strftime("%H:%M:%S")}] Клиент подключился к {addr}:{port}')
    except ConnectionRefusedError:
        server = None
        print(f'[{time.strftime("%H:%M:%S")}] Ошибка! Сервер {addr}:{port} отклонил подключение, проверьте порт или '
              f'сервер для подключения')
    except TimeoutError:
        server = None
        print(f'[{time.strftime("%H:%M:%S")}] Ошибка! Превышено время ожидания ответа от {addr}:{port}')
    except gaierror:
        server = None
        print(f'[{time.strftime("%H:%M:%S")}] Ошибка! Неправильный IP адрес {addr}:{port}, '
              f'проверьте правильность введенного адреса')
    return server


def disconnect_client(server: socket):
    server.close()


def get_args() -> dict:
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
