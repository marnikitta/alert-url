import requests


class Bot:
    def __init__(self, owner_id: int, token: str):
        self.owner_id = owner_id
        self.token = token

    def get_me(self):
        url = f"https://api.telegram.org/bot{self.token}/getMe"
        response = requests.get(url)
        return response.json()

    def send_message(self, chat_id: int, text: str, silent: bool = False):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "disable_notification": silent}
        response = requests.post(url, data=data)
        return response.json()
