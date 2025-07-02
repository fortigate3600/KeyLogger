import requests
from config import TOKEN
import time

chat_id = None
last_update_id = 0

debugging = 1

def initChatID():
    global chat_id
    if chat_id is not None:
        return
    try:
        updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()
        results = updates.get("result", [])
        if not results:
            raise ValueError("error getting chat_id,\n TRY SENDING A MESSAGE TO THE BOT BEFORE STARTING")
        chat_id = results[-1]['message']['chat']['id']
        if debugging:
            print(f"[++]chat id: {chat_id}")
    except Exception as e:
        raise RuntimeError(f"error getting chat_id,: {e},\nTRY SENDING A MESSAGE TO THE BOT BEFORE STARTING")


def sendFromFile(LOG_FILE):
    global chat_id
    if chat_id is None:
        raise RuntimeError("Chat ID not initialized")

    #get the text from the file...
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

    #... to send to the bot
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.get(send_url, params=params)

    if debugging:
        if response.status_code == 200:
            print("[++]Message sent successfully")
        else:
            print("[--]Error sending message", response.text)

#to not check for previous kill command
def syncWithLatestUpdate():
    global last_update_id
    resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates")
    resp.raise_for_status()
    data = resp.json()

    if not data['result']:
        last_update_id = 0
    else:
        last_update_id = data['result'][-1]['update_id']

def getLastMsg(timeout=1):
    global last_update_id

    params = {
        'timeout': timeout,
        'offset': last_update_id + 1
    }
    resp = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params=params)
    resp.raise_for_status()
    data = resp.json()

    if not data['result']:
        return None

    updates = data['result']
    last_update_id = updates[-1]['update_id']
    msg = updates[-1].get('message') or updates[-1].get('edited_message')
    if not msg:
        return None

    return msg.get('text')
