import inspect
import time
from functools import wraps


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


@log
def func_z():
    pass


def main():
    func_z()


if __name__ == '__main__':
    main()
