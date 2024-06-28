# Chat API

Это проект Chat API, который позволяет пользователям регистрироваться, отправлять и получать сообщения, а также управлять своими устройствами. Проект использует Flask для создания RESTful API и SQLite в качестве базы данных.
В будущем я буду добавлять все больше новых фич.
###### Добавю GUI (наверное)
## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/ваш-пользователь/ваш-репозиторий.git
    ```

2. Перейдите в директорию проекта:
    ```sh
    cd ваш-репозиторий
    ```

3. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```

4. Установите необходимые зависимости:
    ```sh
    pip install -r requirements.txt
    ```

5. Запустите приложение:
    ```sh
    python server.py
    ```

## API Эндпоинты

### Регистрация пользователя

**POST /api/regist**

Параметры:
- `name` (str): Имя пользователя.
- `gmail` (str): Электронная почта пользователя.
- `password` (str): Пароль пользователя.

Пример запроса:

```sh
curl -X POST http://127.0.0.1:3000/api/regist -d "name=JohnDoe" -d "gmail=johndoe@example.com" -d "password=securepassword"
```

**POST /api/send_message**

Параметры:

- `name` (str): Имя получателя.
- `message` (str): Текст сообщения.
- `name_devices` (str): Имя устройства отправителя.

Пример запроса:

```sh
curl -X POST http://127.0.0.1:3000/api/send_message -d "name=JohnDoe" -d "message=Hello!" -d "name_devices=device1"
```

**GET /api/get_messages**

Параметры:

- `name_devices` (str): Имя устройства отправителя.

Пример запроса:

```sh
curl -X GET http://127.0.0.1:3000/api/get_messages -d "name_devices=device1"
```

## Профиль пользователя
**POST /api/user**

Параметры:

- `name` (str): Имя получателя.
- `gmail` (str): Электронная почта пользователя.
- `password` (str): Пароль пользователя.
- `name_devices` (str): Имя устройства пользователя.

Пример запроса: 

```sh
curl -X POST http://127.0.0.1:3000/api/user -d "name=JohnDoe" -d "gmail=johndoe@example.com" -d "password=securepassword" -d "name_devices=device1" 
```

## Описание таблиц базы данных 
**Таблица** `users`:

- `id` (INTEGER): Первичный ключ.
- `name` (TEXT): Имя пользователя.
- `gmail`  (TEXT): Электронная почта пользователя.
- `password` (TEXT): Хэш пароля пользователя.

**Таблица** `mes`:

- `name_sender` (TEXT): Имя отправителя сообщения.
- `name` (TEXT): Имя получателя сообщения.
- `message` (TEXT): Текст сообщения.
- `timestamp` (DATETIME): Временная метка отправки сообщения.

**Таблица** `devices`:

- `name` (TEXT): Имя пользователя.
- `name_devices` (TEXT): Имя устройства пользователя.

## Автоматическое удаление старых сообщений

В проекте реализован поток, который удаляет сообщения старше 2 часов каждые 60 минут.

## Лицензия

Этот проект лицензируется в соответствии с условиями MIT License.