"""
Task printer contains a common function to print the task name header
"""
import time


def print_task(task_number: int):
    """
    Выводит в консоль шапку задания с его номером

    :param task_number: номер задания
    """
    print(f'{"=" * 69}\r\n{"=" * 29} Задание {task_number} {"=" * 29}\r\n{"=" * 69}\r\n')


def timed_print(string: str):
    """
    Выводить в консоль строку со временный штампом

    :param string: строка для принта
    """
    print(f'[{time.strftime("%H:%M:%S")}] {string}')
