import json
import requests

headers = {'Content-Type': 'application/json'}

def regist():
    date = {
        "name":"Azamat",
    }

    respons = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(date), headers=headers)
    print(respons.json())

def message():
    date = {
        "name":"Azamat",
        "message":"Hello"
    }
    respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
    print(respons.json())

def get():
    name = "Azamat"
    respons = requests.get(f"http://127.0.0.1:3000/api/get_messages/{name}",headers=headers)
    print(respons.json())

get()