import os
import sys

import pytest

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from homework.lesson3.client import authenticate_client, join_room, leave_room, send_msg


@pytest.mark.parametrize('server, username, password, test_response, result',
[
     (None, 'user', 'password', {
         'response': 202,
         "alert": 'Пользователь user аутентифицирован'
     }, True),
     (None, 'user', 'password', {
         'response': 200,
         "alert": 'Пользователь user уже аутентифицирован'
     }, True),
     (None, 'user1', 'wrong password', {
         'response': 402,
         "error": 'Пользователь user1 не существует или введен неправильный пароль '
     }, False)
 ])
def test_authenticate_client(server, username, password, test_response, result):
    assert authenticate_client(server, username, password, test_response) == result


@pytest.mark.parametrize('server, username, room, test_response, result',
[
     (None, 'user', '#geekbrains', {
         'response': 200,
         "alert": 'Пользователь user присоединился к чату #geekbrains'
     }, True),
     (None, 'user', '#geeks', {
         'response': 200,
         "alert": 'Пользователь user присоединился к чату #geeks'
     }, True)
 ])
def test_join_room(server, username, room, test_response, result):
    assert join_room(server, username, room, test_response) == result


@pytest.mark.parametrize('server, username, room, test_response, result',
[
     (None, 'user', '#geekbrains', {
         'response': 200,
         "alert": 'Пользователь user покинул чат #geekbrains'
     }, True),
     (None, 'user', '#geeks', {
         'response': 200,
         "alert": 'Пользователь user покинул чат #geeks'
     }, True),
     (None, 'user', '#geekbrains', {
         'response': 403,
         "error": 'Пользователь user не состоит в чате #geekbrains'
     }, False),
     (None, 'user', '#geeks1', {
         'response': 400,
         "error": 'Чата #geeks1 не существует'
     }, False),
     (None, 'user', '', {
         'response': 400,
         "error": 'Неуказанна комната для присоединения'
     }, False),
     (None, 'user1', '', {
         'response': 401,
         "error": 'Пользователь user1 не авторизован'
     }, False)
 ])
def test_leave_room(server, username, room, test_response, result):
    assert leave_room(server, username, room, test_response) == result


@pytest.mark.parametrize('server, username, receiver, message, test_response, result',
[
     (None, 'user', '#geekbrains', 'Hello', {
         'response': 200,
         "alert": 'Сообщение от user к #geekbrains доставлено'
     }, True),
     (None, '', '#geekbrains', 'Hello', {
         'response': 400,
         "error": 'Отправитель или адресат неопределенны'
     }, False),
     (None, 'user', '', 'Hello', {
         'response': 400,
         "error": 'Отправитель или адресат неопределенны'
     }, False)
 ])
def test_send_msg(server, username, receiver, message, test_response, result):
    assert send_msg(server, username, receiver, message, test_response) == result
