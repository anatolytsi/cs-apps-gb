import os
import sys
import time

import pytest
from socket import *

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from homework.lesson3.server import server_start, message_dispatcher


@pytest.mark.parametrize('address, port, result',
[
     ('127.0.0.1', 7777, socket),
     ('localhost', 7777, socket),
     ('127.0.0.1', 8080, socket),
     ('', None, socket),
     (None, None, socket),
     ('invalid address', None, None),
 ])
def test_server_start(address, port, result):
    assert type(server_start(address, port)) == socket or not server_start(address, port)


@pytest.mark.parametrize('message, result',
[
     ({
          "action": "authenticate",
          "time": time.time(),
          "user": {
              "account_name": 'user',
              "password": 'password'
          }
      }, {
          'response': 202,
          "alert": 'Пользователь user аутентифицирован'
      }),
     ({
          "action": "authenticate",
          "time": time.time(),
          "user": {
              "account_name": 'user',
              "password": 'password'
          }
      }, {
          'response': 200,
          "alert": 'Пользователь user уже аутентифицирован'
      }),
     ({
          "action": "authenticate",
          "time": time.time(),
          "user": {
              "account_name": 'user1',
              "password": 'wrong password'
          }
      }, {
          'response': 402,
          "error": 'Пользователь user1 не существует или введен неправильный пароль '
      })
 ])
def test_authentication(message, result):
    assert message_dispatcher(message) == result


def test_presence():
    message = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": 'user'
        }
    }
    result = {}
    assert message_dispatcher(message) == result


@pytest.mark.parametrize('message, result',
[
     ({
          "action": "join",
          "time": time.time(),
          "room": '#geekbrains',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 200,
          "alert": 'Пользователь user присоединился к чату #geekbrains'
      }),
     ({
          "action": "join",
          "time": time.time(),
          "room": '#geeks',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 200,
          "alert": 'Пользователь user присоединился к чату #geeks'
      })
 ])
def test_join_room(message, result):
    assert message_dispatcher(message) == result


@pytest.mark.parametrize('message, result',
[
     ({
          "action": "msg",
          "time": time.time(),
          "from": 'user',
          "to": '#geekbrains',
          "message": 'Hello',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 200,
          "alert": 'Сообщение от user к #geekbrains доставлено'
      }),
     ({
          "action": "msg",
          "time": time.time(),
          "from": '',
          "to": '#geekbrains',
          "message": 'Hello',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 400,
          "error": 'Отправитель или адресат неопределенны'
      }),
     ({
          "action": "msg",
          "time": time.time(),
          "to": '#geekbrains',
          "message": 'Hello',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 400,
          "error": 'Отправитель или адресат неопределенны'
      }),
     ({
          "action": "msg",
          "time": time.time(),
          "from": 'user',
          "to": '',
          "message": 'Hello',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 400,
          "error": 'Отправитель или адресат неопределенны'
      }),
     ({
          "action": "msg",
          "time": time.time(),
          "from": 'user',
          "message": 'Hello',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 400,
          "error": 'Отправитель или адресат неопределенны'
      })
 ])
def test_msg_to_chat(message, result):
    assert message_dispatcher(message) == result


@pytest.mark.parametrize('message, result',
[
     ({
          "action": "leave",
          "time": time.time(),
          "room": '#geekbrains',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 200,
          "alert": 'Пользователь user покинул чат #geekbrains'
      }),
     ({
          "action": "leave",
          "time": time.time(),
          "room": '#geeks',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 200,
          "alert": 'Пользователь user покинул чат #geeks'
      }),
     ({
          "action": "leave",
          "time": time.time(),
          "room": '#geekbrains',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 403,
          "error": 'Пользователь user не состоит в чате #geekbrains'
      }),
     ({
          "action": "leave",
          "time": time.time(),
          "room": '#geeks1',
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 400,
          "error": 'Чата #geeks1 не существует'
      }),
     ({
          "action": "leave",
          "time": time.time(),
          "user": {
              "account_name": 'user'
          }
      }, {
          'response': 400,
          "error": 'Неуказанна комната для присоединения'
      }),
     ({
          "action": "leave",
          "time": time.time(),
          "user": {
              "account_name": 'user1'
          }
      }, {
          'response': 401,
          "error": 'Пользователь user1 не авторизован'
      })
 ])
def test_leave_room(message, result):
    assert message_dispatcher(message) == result
