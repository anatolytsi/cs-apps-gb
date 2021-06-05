# Урок 2. Файловое хранение данных
### Задание 1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
Клиент отправляет запрос серверу --> сервер отвечает соответствующим кодом результата.

Клиент и сервер должны быть реализованы в виде отдельных скриптов,
содержащих соответствующие функции.

Функции клиента:
* сформировать presence-сообщение;
* отправить сообщение серверу;
* получить ответ сервера;
* разобрать сообщение сервера;
* параметры командной строки скрипта `client.py <addr> [<port>]`:
    - addr — ip-адрес сервера;
    - port — tcp-порт на сервере, по умолчанию 7777.

Функции сервера:
* принимает сообщение клиента;
* формирует ответ клиенту;
* отправляет ответ клиенту;
* имеет параметры командной строки:
    - `-p <port>` — TCP-порт для работы (по умолчанию использует 7777);
    - `-a <addr>` — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).

##### Функция `get_data()`:
```python
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
```

##### Функция `write_to_csv()`:
```python
def write_to_csv(csv_path: str):
    """
    Открывает/создает файл по указанному пути и записывает туда данные, полученные функцией get_data()
    :param csv_path: путь к csv файлу
    """
    filepath = f'{CURRENT_DIR}\\{csv_path if ".csv" in csv_path else f"{csv_path}.csv"}'
    with open(filepath, 'w', newline='\n', encoding='utf-16') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(get_data())
```

##### Работа программы:
```python
write_to_csv('test')
```

##### Файл `test.csv`:

|Изготовитель системы|Название ОС|Код продукта|Тип системы|
|:--------------------:|:-----------:|:------------:|-----------:|
|Microsoft Corporation	|Microsoft Windows 7 Профессиональная| 	00971-OEM-1982661-00231	|x64-based PC|
|Microsoft Corporation	|Microsoft Windows 10 Professional|	00971-OEM-1982661-00231	|x64-based PC|
|Microsoft Corporation	|Microsoft Windows 8.1 Professional|	00971-OEM-1982661-00231	|x86-based PC|


### Задание 2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. 
Для этого:

<ol type="a">
<li>Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена
(price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;</li>
<li>Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.</li>
</ol>

##### Функция `write_order_to_json()`:
```python
def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: float):
    """
    Добавляет определенный товар в заказы (в JSON)

    :param item: название товара
    :param quantity: количество товара
    :param price: цена товара
    :param buyer: покупатель
    :param date: время заказа
    """
    data = []
    filepath = f'{CURRENT_DIR}\\{ORDERS_JSON}'
    with open(filepath) as f:
        data = json.load(f)
        data['orders'].append({'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date})

    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=4))
```

##### Работа программы:
```python
write_order_to_json('Пальто', 1, 20000, 'Человек Человекович', time.time())
```

##### Файл `orders.json`:
```json
{
    "orders": [
        {
            "item": "\u041f\u0430\u043b\u044c\u0442\u043e",
            "quantity": 1,
            "price": 20000,
            "buyer": "\u0427\u0435\u043b\u043e\u0432\u0435\u043a \u0427\u0435\u043b\u043e\u0432\u0435\u043a\u043e\u0432\u0438\u0447",
            "date": 1622383062.1543055
        }
    ]
}
```

### Задание 3. Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:

<ol type="a">
<li>Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке
ASCII (например, €);</li>
<li>Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с
помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;</li>
<li>Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.</li>
</ol>

##### Функция `get_data()`:
```python
def get_data() -> dict:
    """
    Читает JSON-файл с заказами и выдает данные

    :return: словарь данных
    """
    filepath = f'{CURRENT_DIR}\\{ORDERS_JSON}'
    with open(filepath) as f:
        return json.load(f)
```

##### Функция `save_and_verify()`:
```python
def save_and_verify(filename: str, data: dict = None):
    """
    Сохраняет принятые данные в указанный yaml документ в папке скрипта

    :param filename: имя или путь к файлу в папке скрипта
    :param data: словарь данных
    """
    filepath = f'{CURRENT_DIR}\\{filename if ".yaml" in filename else f"{filename}.yaml"}'

    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    print(f'* Прочитанный файл {filepath}:\r\n')
    with open(filepath) as f:
        print(f.read())
```

##### Работа программы:
```python
save_and_verify('file', get_data())
```

##### Чтение файла `file.yaml` и вывод его в консоли:
```yaml
orders:
- buyer: Человек Человекович
  date: 1622383062.1543055
  item: Пальто
  price: 20000
  quantity: 1
```
