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
        a = input("какое из этих эмодзи хотите отправить")
        if a == "1":
            g = emoji.emojize("1: :grinning_face:") 
        if a == "2":
            c = emoji.emojize("2: :grinning_face_with_sweat:")
        else:
            print("пока есть только два")
    else:
        print("Ладно(")
    m = nes + g
    date = {
        "name":"Magnat",
        "message": m
    }
    respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
    print(respons.json())
    
message()