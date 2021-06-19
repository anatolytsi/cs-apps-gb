# Урок 6. Декораторы и продолжение работы с сетью

### Задание 1. Продолжая задачу логирования, реализовать декоратор @log, фиксирующий обращение к декорируемой функции. Он сохраняет ее имя и аргументы.

##### Вывод логгера сервера в файле:

```text
2021-06-15 22:08:10,190 DEBUG    server     Была вызвана функция main с аргументами (), {}
2021-06-15 22:08:10,191 DEBUG    server     Была вызвана функция get_args с аргументами (), {}
2021-06-15 22:08:10,209 DEBUG    server     Была вызвана функция server_start с аргументами (None, None), {}
2021-06-15 22:08:10,211 INFO     server     Сервер запущен по адресу :7777
2021-06-15 22:08:10,212 DEBUG    server     Была вызвана функция server_listen с аргументами (<socket.socket fd=312, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 7777)>,), {}
2021-06-15 22:08:25,076 INFO     server     Соединение с клиентом установленно
2021-06-15 22:08:25,086 DEBUG    server     Была вызвана функция message_dispatcher с аргументами ({'action': 'authenticate', 'time': 1623787705.0811276, 'user': {'account_name': 'user', 'password': 'password'}},), {}
2021-06-15 22:08:25,087 DEBUG    server     Была вызвана функция message_authenticate с аргументами ({'action': 'authenticate', 'time': 1623787705.0811276, 'user': {'account_name': 'user', 'password': 'password'}},), {}
2021-06-15 22:08:25,087 INFO     server     202: Пользователь user аутентифицирован
...
```

##### Вывод логгера клиента в файле:

```text
2021-06-15 22:08:12,538 DEBUG    client     Была вызвана функция main с аргументами (), {}
2021-06-15 22:08:12,538 DEBUG    client     Была вызвана функция get_args с аргументами (), {}
2021-06-15 22:08:25,055 DEBUG    client     Была вызвана функция main с аргументами (), {}
2021-06-15 22:08:25,056 DEBUG    client     Была вызвана функция get_args с аргументами (), {}
2021-06-15 22:08:25,074 DEBUG    client     Была вызвана функция connect_client с аргументами ('localhost', None), {}
2021-06-15 22:08:25,076 INFO     client     Клиент подключился к 127.0.0.1:7777
2021-06-15 22:08:25,081 DEBUG    client     Была вызвана функция authenticate_client с аргументами (<socket.socket fd=332, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 57325), raddr=('127.0.0.1', 7777)>, 'user', 'password'), {}
2021-06-15 22:08:25,081 INFO     client     Аутентификация user...
2021-06-15 22:08:25,084 DEBUG    client     Была вызвана функция send_data_to_server с аргументами (<socket.socket fd=332, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 57325), raddr=('127.0.0.1', 7777)>, {'action': 'authenticate', 'time': 1623787705.0811276, 'user': {'account_name': 'user', 'password': 'password'}}), {}
2021-06-15 22:08:25,086 DEBUG    client     Была вызвана функция get_response_from_server с аргументами (<socket.socket fd=332, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 57325), raddr=('127.0.0.1', 7777)>, None), {}
...
```

Полные дебаг выводы см. в соответствующих файлах.

### Задание 2. В декораторе @log реализовать фиксацию функции, из которой была вызвана декорированная. Если имеется такой код:

```python
@log
def func_z():
 pass

def main():
 func_z()
```

...в логе должна быть отражена информация:
"<дата-время> Функция func_z() вызвана из функции main"

### Реализация

Функция была реализована для принятия аргументов декорируемой функции с целью стандартизации последней.

#### Декоратор

```python
def log(func):
    """
    Декоратор для логинга вызова функций
    :param func: декорируемая функция
    """""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Функция - обертка для декорируемой функции
        :param args: аргументы декорируемой функции
        :param kwargs: кварги декорируемой функции
        """
        print(f'{time.strftime("%H:%M:%S")} Функция {func.__name__}() была вызвана из функции {inspect.stack()[1][3]}')
        return func(*args, **kwargs)

    return wrapper
```

##### Вывод в консоли

```console
22:14:37 Функция func_z() была вызвана из функции main
```
