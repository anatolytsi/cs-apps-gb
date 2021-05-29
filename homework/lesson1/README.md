### Задание 1.
Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и
также проверить тип и содержимое переменных.

##### Слово "разработка":
```python
compare_string_with_unicode('разработка', '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430')
```
Вывод в консоли:
```python
* Строка "разработка":
	- cтроковое значение: "разработка", тип: <class 'str'>, длина: 10
	- unicode: "разработка", тип: "<class 'str'>", длина: 10
	- они идентичны друг другу!
```

##### Слово "сокет":
```python
compare_string_with_unicode('сокет', '\u0441\u043e\u043a\u0435\u0442')
```
Вывод в консоли:
```python
* Строка "сокет":
	- cтроковое значение: "сокет", тип: <class 'str'>, длина: 5
	- unicode: "сокет", тип: "<class 'str'>", длина: 5
	- они идентичны друг другу!
```

##### Слово "декоратор":
```python
compare_string_with_unicode('декоратор', '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440')
```
Вывод в консоли:
```python
* Строка "декоратор":
	- cтроковое значение: "декоратор", тип: <class 'str'>, длина: 9
	- unicode: "декоратор", тип: "<class 'str'>", длина: 9
	- они идентичны друг другу!
```

### Задание 2
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

##### Слово "class":
```python
print_string_bytes_info('class')
```
Вывод в консоли:
```python
* Строка class
	- в байтах: b'class'
	- тип: <class 'bytes'>
	- длина: 5
```

##### Слово "function":
```python
print_string_bytes_info('function')
```
Вывод в консоли:
```python
* Строка method
	- в байтах: b'method'
	- тип: <class 'bytes'>
	- длина: 6
```

##### Слово "method":
```python
print_string_bytes_info('method')
```

Вывод в консоли:
```python
*********************************************************************
* Строковое значение: "method"
* В байтах: b'method', тип: <class 'bytes'>, длина: 6
*********************************************************************
```

### Задание 3
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

##### Слово "attribute":
```python
assert_string_to_bytes('attribute')
```

Вывод в консоли:
```python
* Строка "attribute" в байтах: b'attribute'
```

##### Слово "класс":
```python
assert_string_to_bytes('класс')
```

Вывод в консоли:
```python
* Строка "класс" не может быть конвертирована при помощи b"" или с кодировкой ASCII
```

##### Слово "функция":
```python
assert_string_to_bytes('функция')
```

Вывод в консоли:
```python
* Строка "функция" не может быть конвертирована при помощи b"" или с кодировкой ASCII
```

##### Слово "класс":
```python
assert_string_to_bytes('функция')
```

Вывод в консоли:
```python
* Строка "type" в байтах: b'type'
```

### Задание 4
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и
выполнить обратное преобразование (используя методы encode и decode).

##### Слово "разработка":
```python
encode_decode_string('разработка')
```

Вывод в консоли:
```python
* Строка "разработка":
	- в закодированном виде: b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
	- после декодинга: "разработка"
```

##### Слово "администрирование":
```python
encode_decode_string('администрирование')
```

Вывод в консоли:
```python
* Строка "администрирование":
	- в закодированном виде: b'\xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5'
	- после декодинга: "администрирование"
```

##### Слово "protocol":
```python
encode_decode_string('protocol')
```

Вывод в консоли:
```python
* Строка "protocol":
	- в закодированном виде: b'protocol'
	- после декодинга: "protocol"
```

##### Слово "standard":
```python
encode_decode_string('standard')
```

Вывод в консоли:
```python
* Строка "standard":
	- в закодированном виде: b'standard'
	- после декодинга: "standard"
```


### Задание 5
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
кириллице.

##### Сайт "yandex.ru":
```python
ping_website('yandex.ru')
```

Вывод в консоли:
```python
* Сайт yandex.ru:
	- Pinging yandex.ru [5.255.255.88] with 32 bytes of data:
	- Reply from 5.255.255.88: bytes=32 time=55ms TTL=245
	- Reply from 5.255.255.88: bytes=32 time=52ms TTL=245
	- Reply from 5.255.255.88: bytes=32 time=52ms TTL=245
	- Reply from 5.255.255.88: bytes=32 time=52ms TTL=245
	- Ping statistics for 5.255.255.88:
	-     Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
	- Approximate round trip times in milli-seconds:
	-     Minimum = 52ms, Maximum = 55ms, Average = 52ms
```

##### Сайт "youtube.com":
```python
ping_website('youtube.com')
```

Вывод в консоли:
```python
* Сайт youtube.com:
	- Pinging youtube.com [142.250.185.206] with 32 bytes of data:
	- Reply from 142.250.185.206: bytes=32 time=18ms TTL=113
	- Reply from 142.250.185.206: bytes=32 time=22ms TTL=113
	- Reply from 142.250.185.206: bytes=32 time=21ms TTL=113
	- Reply from 142.250.185.206: bytes=32 time=17ms TTL=113
	- Ping statistics for 142.250.185.206:
	-     Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
	- Approximate round trip times in milli-seconds:
	-     Minimum = 17ms, Maximum = 22ms, Average = 19ms
```


### Задание 6
Создать текстовый файл `test_file.txt`, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.

##### Запись в файл `test_file.txt`:
```python
write_to_file('test_file.txt', ['сетевое программирование', 'сокет', 'декоратор'])
```

##### Чтение из файла `test_file.txt`:
```python
read_file_in_utf8('test_file.txt')
```

Вывод в консоли:
```python
* Пишем в файл test_file.txt...
	- Кодировка записанного файла: cp1251
* Читаем файл test_file.txt...
	- Кодировка открытого файла: utf-8
	- Ошибка декодирования данных!
```
