"""

"""
import argparse
import pickle
import time
from socket import *


def get_response_from_server(server: socket):
    data = server.recv(1024)
    response = pickle.loads(data)
    if 'error' in response:
        print(f'Сервер ответил ошибкой: {response["response"]} {response["error"]}')
    elif 'alert' in response:
        print(f'Сервер ответил: {response["response"]} {response["alert"]}')


def authenticate_client(server: socket, username: str, password: str):
    msg = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": username,
            "password": password
        }
    }
    print(f'Аутентификация {username}...')
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
    print(f'Шлем presence...')
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
    print(f'Шлем сообщение от {sender} к {receiver}: {message}')
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
    print(f'Пользователь {username} присоединяется к чату {room}...')
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
    print(f'Пользователь {username} выходит из чата {room}...')
    server.send(pickle.dumps(msg))
    get_response_from_server(server)


def connect_client(addr: str, port: int = 7777) -> socket:
    port = port if port else 7777
    server = None
    try:
        if addr:
            addr = '127.0.0.1' if addr == 'localhost' else addr
            inet_aton(addr)
        server = socket(AF_INET, SOCK_STREAM)
        server.connect((addr, port))
        print(f'Клиент подключился к {addr}:{port}')
    except error:
        print(f'Ошибка! Неправильный IP адрес {addr}:{port}, проверьте правильность введенного адреса')
    return server


def disconnect_client(server: socket):
    server.close()


def make_server_request(addr: str, port: int, func, *args):
    server = connect_client(addr, port)
    func(server, *args)
    disconnect_client(server)


def main():
    user = 'user'
    parser = argparse.ArgumentParser(description='Простой клиент на Python')
    parser.add_argument('-a', '--address',
                        help='IP адрес сервера',
                        required=True)
    parser.add_argument('-p', '--port',
                        help='Порт сервера, по умолчанию использует 7777',
                        required=False)
    args = vars(parser.parse_args())
    make_server_request(args['address'], args['port'], authenticate_client, user, 'password')
    make_server_request(args['address'], args['port'], send_presence, user)
    make_server_request(args['address'], args['port'], join_room, user, '#geeks')
    make_server_request(args['address'], args['port'], send_msg, user, '#geeks', 'Всем привет в этом чатике!')
    make_server_request(args['address'], args['port'], send_msg, user, '#geeks', 'Ну и больно надо...')
    make_server_request(args['address'], args['port'], leave_room, user, '#geekbrains')


if __name__ == '__main__':
    main()
