import json
import requests
import time
import hashlib

token = '6338630872:AAFekL6uidz3pGqGVLxOduK-zDeOBMZ5kwM'
base_link = f'https://api.telegram.org/bot{token}/'
file_storage = 'bot_answered_messages.txt'
answered_messages = []
counting_mode = False

bus_services = {
    "044p": {
        "departure_city": "Kyiv",
        "arrival_city": "Lviv",
        "departure_time": "12:00",
        "arrival_time": "20:00",
        "price": 400,
        "total_number_of_places": 40,
    },
    "223lk": {
        "departure_city": "Lviv",
        "arrival_city": "Kyiv",
        "departure_time": "14:30",
        "arrival_time": "23:00",
        "price": 500,
        "total_number_of_places": 40,
    }
}

orders = [
    {
        "id": "hrejer54j43hd",
        "name": "Гончарук А.Г.",
        "bus_service_id": "044p"
    },
    {
        "id": "h6jh578jk6kl6",
        "name": "Петренко Г.Г.",
        "bus_service_id": "044p"
    }
]


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
            result = ''
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


def cfp(bus_service_id):
    booked_places = 0

    for order in orders:
        if order['bus_service_id'] == bus_service_id:
            booked_places += 1

    free_places = bus_services[bus_service_id]['total_number_of_places'] - booked_places

    return free_places


booking_step = 0

while True:
    update = get_update()

    if update != 'No new notifications last day':
        update_id = get_update_id(update)

        if update_id not in answered_messages:
            answered_messages.append(update_id)
            text = get_message_text(update)
            chat_id = get_chat_id(update)
            print(f"Last notification: {text} from user (id): {chat_id}")

            if booking_step == 0:

                if text == '/help' or text == '/Help':
                    res = 'You can run these commands:\n' \
                          '/help\n'\
                          '/schedule\n\n'

                if text == '/schedule':
                    res = 'grafic\n\n'
                    for bus_service_id, bus_service_info in bus_services.items():
                        res += 'Reys ' + bus_service_id + '\n'

                        for key, value in bus_service_info.items():
                            res += key + ": " + str(value) + '\n'

                        res += 'free_places' + str(cfp(bus_service_id)) + '\n\n'

                if text == '/book':
                    send_message(chat_id, 'Напишіть ПІБ та номер рейсу через кому')
                    booking_step = 1
            else:
                order_info = text.split(',')
                name = order_info[0]
                bus_service_id = order_info[1]
                name.strip()
                bus_service_id.strip()
                hash_id = hashlib.md5((name + bus_service_id).encode('UTF-8')).hexdigest()
                send_message(chat_id, 'thank you')

                orders.append({
                    "id": hash_id,
                    "name": name,
                    "bus_service_id": bus_service_id

                })
                print(orders)

                booking_step = 0

            send_message(chat_id, res)
    time.sleep(1)
