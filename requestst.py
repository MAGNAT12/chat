import json
import requests
import emoji
import platform

headers = {'Content-Type': 'application/json'}
name_devices = platform.node()

def regist():
    date = {
        "name":"Magnat",
        "gmail":"rizamatmu@gmail.com",
        "password":"123456789",
    }

    respons = requests.post("http://127.0.0.1:3000/api/regist", data=json.dumps(date), headers=headers)
    print(respons.json())


def message():
    date = {
        "name":"Magnat",
        "message":"привет",
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


def profil():
    date = {
        "name":"Magnat",
        "gmail":"rizamatmu@gmail.com",
        "password":"123456789",
        "name_devices": name_devices
    }

    respons = requests.post("http://127.0.0.1:3000/api/user", data=json.dumps(date), headers=headers)
    print(respons.json())

profil()

