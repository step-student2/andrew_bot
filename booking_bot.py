import json
import requests
import time

token = '6338630872:AAFekL6uidz3pGqGVLxOduK-zDeOBMZ5kwM'
base_link = f'https://api.telegram.org/bot{token}/'
file_storage = 'bot_answered_messages.txt'
answered_messages = []
counting_mode = False

def read_answ_mess():
    global answered_messages
    with open(file_storage, 'r') as f:
        answered_messages_str = f.read()
        try:
            answered_messages = json.loads(answered_messages_str)
        except:
            pass
def write_answ_mess():
    with open(file_storage, 'w') as f:
        f.write(json.dumps(answered_messages))

def get_update():
    link = base_link + 'getUpdates?offset=-1'
    response = requests.get(link)
    response_dict = response.json()

    try:
        if not response_dict['result']:
            return ''
        else:
            result = response_dict['result'][0]

        return result
    except Exception:
        return 'Oops! Something went wrong...'

def get_message_text(update):
    return update['message']['text']

def get_chat_id(update):
    return update['message']['chat']['id']

def get_update_id(update):
    return update['update_id']

def send_message(id, text):
    link = base_link + f'sendMessage?chat_id={id}&text={text}'
    requests.get(link)

while True:
    read_answ_mess()
    update = get_update()

    if update != 'No new notifications last day':
        update_id = get_update_id(update)

        if update_id not in answered_messages:
            answered_messages.append(update_id)
            text = get_message_text(update)
            write_answ_mess()
            chat_id = get_chat_id(update)
            print(text)



    time.sleep(1)
