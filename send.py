import requests
from config import TOKEN

def send(LOG_FILE):
    debugging = 0
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            TEXT = file.read()
    except Exception as e:
        print("Error reading file:", e)
        return

    # get chat_id
    try:
        updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
        chat_id = updates['result'][-1]['message']['chat']['id']
    except Exception as e:
        print("error getting chat_id:", e)
        return

    # send
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": TEXT}
    response = requests.get(send_url, params=params)

    if debugging:
        if response.status_code == 200:
            print("message sent")
        else:
            print("Error sending message", response.text)
