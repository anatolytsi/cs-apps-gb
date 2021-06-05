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
import time
from socket import *

online_users = []
chats = {}


def send_msg(client: socket, response: dict):
    client.send(pickle.dumps(response))


def message_dispatcher(msg: dict) -> dict:
    response_code = None
    response_text = None
    response_is_error = None
    if msg['action'] == 'authenticate':
        if msg['user']['account_name'] not in online_users:
            # TODO нормальную проверку пароля
            if msg['user']['password'] == 'password':
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


def server_listen(addr: str = '', port: int = 7777):
    addr = addr if addr else ''
    port = port if port else 7777
    if addr:
        addr = '127.0.0.1' if addr == 'localhost' else addr
        try:
            inet_aton(addr)
        except error:
            print(f'[{time.strftime("%H:%M:%S")}] Ошибка! Неправильный IP адрес {addr}:{port}, '
                  f'проверьте правильность введенного адреса')
            return
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((addr, int(port)))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print(f'[{time.strftime("%H:%M:%S")}] Сервер запущен по адресу {addr}:{port}')
    while True:
        client, addr = s.accept()
        while True:
            try:
                data = client.recv(1024)
                response = message_dispatcher(pickle.loads(data))
                send_msg(client, response)
            except EOFError:
                break
            except ConnectionResetError:
                # Клиент вышел сам
                break
        client.close()


def get_args() -> dict:
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
    server_listen(args['address'], args['port'])


if __name__ == '__main__':
    main()
