import requests


r = requests.get('https://api.telegram.org/bot6085518492:AAH_kIEdPTWDXAEoDgDeO0N-ZvxMUr9w7NQ/sendMessage?chat_id=2003605393&text=hello andrew!'
                 )

print(r.json())




