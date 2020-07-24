import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

V = 5.92
VK_TOKEN = os.getenv("VK_TOKEN")
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
client = Client(account_sid=ACCOUNT_SID, auth_token=AUTH_TOKEN)
NUMBER_FROM = os.getenv("NUMBER_FROM")
NUMBER_TO = os.getenv("NUMBER_TO")
method = "users.get"
VK_BASE_URL_TEMPLATE = f'https://api.vk.com/method/{method}'

def get_status(user_id):
    params = {
        "v": V,
        "user_ids": user_id,
        "fields": "online",
        "access_token": VK_TOKEN
    }
    try:
        online = requests.post(VK_BASE_URL_TEMPLATE, params=params)
        online = online.json()["response"][0]["online"]
    except requests.exceptions.RequestException:
        online = 0
    return online  


def sms_sender(sms_text): 
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )   
    return message.sid 


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
