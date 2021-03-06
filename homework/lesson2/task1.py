"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в
него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;

c.Проверить работу программы через вызов функции write_to_csv().
"""
import os
import sys
import regex
import csv

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from homework.common.printer import print_task

CURRENT_DIR = os.path.dirname(__file__)

files = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def write_to_csv(csv_path: str):
    """
    Открывает/создает файл по указанному пути и записывает туда данные, полученные функцией get_data()
    :param csv_path: путь к csv файлу
    """
    filepath = f'{CURRENT_DIR}\\{csv_path if ".csv" in csv_path else f"{csv_path}.csv"}'
    with open(filepath, 'w', newline='\n', encoding='utf-16') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(get_data())


def get_data() -> list:
    """
    Извлекает информацию о системе из указанных в списке files текстовых файлах и подготавливает ее под csv формат
    """
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    for file in files:
        filepath = f'{CURRENT_DIR}\\{file if ".txt" in file else f"{file}.txt"}'
        with open(filepath) as f:
            content = f.read()

        # Используется библиотека regex тк lookbehind в re библиотеке не допускает мэтчей неизвестной длины
        os_prod = regex.search(r'(?<=(Изготовитель ОС:).*[ \t]\b).*', content).captures()[0]
        os_name = regex.search(r'(?<=(Название ОС:).*[ \t]\b).*', content).captures()[0]
        os_code = regex.search(r'(?<=(Код продукта:).*[ \t]\b).*', content).captures()[0]
        os_type = regex.search(r'(?<=(Тип системы:).*[ \t]\b).*', content).captures()[0]
        main_data.append([os_prod, os_name, os_code, os_type])
    return main_data


def main():
    print_task(1)
    write_to_csv('test')


if __name__ == '__main__':
    main()
