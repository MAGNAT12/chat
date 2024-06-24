import json
import requests
import emoji

headers = {'Content-Type': 'application/json'}

def regist():
    date = {
        "name":"Magnat",
        "gmail":"rizamatmu@gmail.com",
        "password":"123456789"
    }

    respons = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(date), headers=headers)
    print(respons.json())

def message():
    date = {
        "name":"Magnat",
        "message":"привет"
    }
    respons = requests.post("http://127.0.0.1:3000/api/send_message", data=json.dumps(date), headers=headers)
    print(respons.json())

def get():
    name = "Magnat"
    respons = requests.get(f"http://127.0.0.1:3000/api/get_messages/{name}")
    print(respons.json())

regist()
