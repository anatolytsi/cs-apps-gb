from functools import wraps


def log(func):
    """Декоратор может принимать аргументы для декорируемой функции"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Была вызвана функция {func.__name__} с аргументами {args}, {kwargs}')
        return func(*args, **kwargs)

    return wrapper
