import emoji
import json
import requests
headers = {'Content-Type': 'application/json'}

nes = input("Введите сообщение: ")
em = input("Вы хотите добавить эмидзи: ")

def message():
    if em == 'да':
        print(emoji.emojize("1: :grinning_face:"))
        print(emoji.emojize("2: :grinning_face_with_sweat:"))
        a = input("какое из этих эмодзи хотите отправить: ")
        if a == "1":
            g = emoji.emojize(":grinning_face:") 
            m = nes + g
            date = {
                "name":"Magnat",
                "message": m
            }
            respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
            print(respons.json())
        if a == "2":
            c = emoji.emojize(":grinning_face_with_sweat:")
            m = nes + c
            date = {
                "name":"Magnat",
                "message": m
            }
            respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
            print(respons.json())
        else:
            print("Болеше нету сори)")
    else:
        date = {
                "name":"Magnat",
                "message": nes
            }
        respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
        print(respons.json())
        
message()