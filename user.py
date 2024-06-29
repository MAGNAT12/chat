import json
import requests
import platform

headers = {'Content-Type': 'application/json'}
name_devices = platform.node()

def regist(name, gmail, password):
    date = {
        "name":name,
        "gmail":gmail,
        "password":password,
    }

    respons = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(date), headers=headers)
    print(respons.json())


def message(name, messag):
    date = {
        "name":name,
        "message":messag,
        "name_devices": name_devices
    }
    respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
    print(respons.json())

def get():
    date = {
        "name_devices":name_devices
    }
    respons = requests.get(f"http://127.0.0.1:3000/api/get_messages", data = json.dumps(date), headers=headers)
    print(respons.json())


def profil(name, gmail, password):
    date = {
        "name":name,
        "gmail":gmail,
        "password":password,
        "name_devices": name_devices
    }

    respons = requests.post("http://127.0.0.1:3000/api/user", data=json.dumps(date), headers=headers)
    print(respons.json())

if __name__ == "__main__":
    while True:
        print("1. Регистрация")
        print("2. Ввохд в профиль")
        print("3. Отправить сообщение")
        print("4. Получить сообщение")
        print("5. Выход")
        a = input("Введите цифру: ")
        if a == '1':
            name = input("Введите имя: ")
            gmail = input("Введите gmail: ")
            password = input("Введите пароль: ")
            regist(name, gmail, password)
        elif a == "2":
            name = input("Введите имя: ")
            gmail = input("Введите gmail: ")
            password = input("Введите пароль: ")
            profil(name, gmail, password)
        elif a == '3':
            name = input("Введите имя каму хотите отправить сообщение: ")
            messag = input("Введите сообщение: ")
            message(name, messag)
        elif a == '4':
            get()
        elif a == '5':
            break
        else:
            print("Введите цифру")