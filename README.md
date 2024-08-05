# Чат Приложение

Этот проект представляет собой простое чат-приложение, использующее Flask и SQLite. В проект входят как серверная, так и клиентская части. Серверная часть реализована с помощью Flask и SQLite, а клиентская — с помощью Tkinter для графического интерфейса.

## Серверная часть (Flask API)

### Обзор

Серверная часть состоит из приложения Flask (`server.py`), которое предоставляет RESTful API для регистрации пользователей, отправки сообщений и получения сообщений. Для хранения данных используется SQLite.

### Эндпоинты

1. **Регистрация пользователя**
   - **Эндпоинт:** `/api/regist`
   - **Метод:** `POST`
   - **Параметры:**
     - `name`: Имя пользователя
     - `gmail`: Электронная почта пользователя
     - `password`: Пароль пользователя
   - **Ответ:** 
     - `200 OK`, если регистрация прошла успешно
     - `400 Bad Request`, если пользователь уже существует

2. **Отправка сообщения**
   - **Эндпоинт:** `/api/send_message`
   - **Метод:** `POST`
   - **Параметры:**
     - `name_sender`: Имя отправителя
     - `name`: Имя получателя
     - `message`: Содержание сообщения
     - `token`: Токен аутентификации пользователя
   - **Ответ:** 
     - `200 OK`, если сообщение успешно отправлено
     - `400 Bad Request`, если токен неверен или получатель не существует

3. **Получение сообщений**
   - **Эндпоинт:** `/api/get_messages`
   - **Метод:** `GET`
   - **Параметры:**
     - `token`: Токен аутентификации пользователя
   - **Ответ:**
     - `200 OK` с списком сообщений, если успешно
     - `400 Bad Request`, если сообщения не найдены или токен неверен

4. **Профиль пользователя**
   - **Эндпоинт:** `/api/user`
   - **Метод:** `POST`
   - **Параметры:**
     - `name`: Имя пользователя
     - `gmail`: Электронная почта пользователя
     - `password`: Пароль пользователя
     - `token`: Токен аутентификации пользователя
   - **Ответ:**
     - `200 OK`, если профиль успешно обновлен
     - `400 Bad Request`, если неверные учетные данные

### Запуск сервера

Чтобы запустить сервер Flask, выполните:

```bash
python server.py
```

Сервер запустится по адресу `http://127.0.0.1:3000`

## Клиентская часть (Tkinter GUI)

### Обзор 

Клиентская часть состоит из скриптов Tkinter для регистрации и входа в систему.

### Скрипты

1. `register.py`
    - Предоставляет форму регистрации, где пользователи могут зарегистрироваться, введя свое имя, электронную почту и пароль.

2. `login.py`
    - Предоставляет форму для входа, где пользователи могут войти в систему, используя свои учетные данные.

3. `profil.py`
    - Заготовка для управления профилем пользователя после входа в систему. (незавершон)

### Запуск GUI

Чтобы запустить графический интерфейс Tkinter, выполните соответствующий скрипт:
```bash
python GUI/register.py
```

### Дополнительные скрипты
- `requestst.py`: Скрипт для тестирования API-эндпоинтов с использованием requests.
- `user.py`: Скрипт для взаимодействия с API и управления пользователями

## Лицензия

Этот проект лицензирован под лицензией MIT. См. файл ([LICENSE](https://github.com/MAGNAT12/chat/blob/main/LICENSE)) для получения дополнительных сведений.