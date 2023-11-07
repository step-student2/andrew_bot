import datetime
import json
import random
import requests
import time
import webbrowser
from datetime import datetime

token = '6085518492:AAH_kIEdPTWDXAEoDgDeO0N-ZvxMUr9w7NQ'
base_link = f'https://api.telegram.org/bot{token}/'
tempstorage = f"https://api.telegram.org/bot/getMe{token}"
file_storage = 'bot_answered_messages.txt'
answered_messages = []
counting_mode = False
site_openning = False

def read_answ_mess():
    global answered_messages
    with open(file_storage, 'r') as f:
        answered_messages_str = f.read()
        answered_messages = json.loads(answered_messages_str)

def write_answ_mess():
    with open(file_storage, 'w') as f:
        f.write(json.dumps(answered_messages))

def get_update():
    link = base_link + 'getUpdates?offset=-1'
    response = requests.get(link)
    response_dict = response.json()

    try:
        if not response_dict['result']:
            result = 'No new notifications last day'
        else:
            result = response_dict['result'][0]

        return result
    except Exception:
        return 'Oops! Something went wrong...'

def get_message_text(update):
    return update['message']['text']

def get_chat_id(update):
    return update['message']['chat']['id']

# def get_username(update):
#     return  update['message']['']

def get_update_id(update):
    return update['update_id']

def send_message(id, text):
    link = base_link + f'sendMessage?chat_id={id}&text={text}'
    requests.get(link)

while True:
    global  can_next1, can_id
    can_next1 = False
    can_id = False
    update = get_update()

    if update != 'No new notifications last day':
        update_id = get_update_id(update)

        if update_id not in answered_messages:
            answered_messages.append(update_id)
            temp = tempstorage
            text = get_message_text(update)
            chat_id = get_chat_id(update)

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            print(f"Last notification: {text} from user (id): {chat_id} at {current_time}")

            print(temp)
            send_message(chat_id, input("answer: "))

    else:
        print("no new notifications")




    time.sleep(0.2)


