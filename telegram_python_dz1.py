import requests


def update(token):
    ssilka = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(ssilka)
    data = response.json()

    if 'result' in data and len(data['result']) > 0:
        last_update = data['result'][-1]
        return last_update

    return None


def message(messagee):
    text = messagee['text']
    print(f"получено message: {text}")


def main():
    token = "6085518492:AAH_kIEdPTWDXAEoDgDeO0N-ZvxMUr9w7NQ"
    last_update = update(token)

    if last_update != None and 'message' in last_update:
        message(last_update['message'])


main()
