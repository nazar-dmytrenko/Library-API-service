import requests


def send_telegram_message(bot_token, chat_id, message):

    """
        This function is used to send a telegram message with taken message
    """

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.get(url, params=params)
    return response.json()
