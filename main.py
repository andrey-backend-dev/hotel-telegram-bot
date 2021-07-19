import requests
import re
import json
import telebot
import nltk
import subprocess
from telebot import TeleBot
from typing import List, Dict, Union, Optional
from dotenv import load_dotenv
import os
import shlex
load_dotenv()
# BOT INFO: @hotelanalysisbot
TOKEN: str = os.getenv('TOKEN')
bot: TeleBot = telebot.TeleBot(TOKEN)
with open('botconfig.json', 'r', encoding='utf-8') as json_file:
    BOT_CONFIG: Dict[str, Union[Dict[str, Dict[str, Union[str, List]]], str]] = json.load(json_file)
message_to_another_script = None
max_hotel_count: Optional[int] = None
hotel_count: Optional[int] = None
city: Optional[str] = None


def clean(text: str) -> str:
    """
    Function which is cleaning given text.
    :param text: text need to clean
    :return: cleaned text
    :rtype: str
    """
    text = text.lower()
    text = re.sub(r'[0-9]', '', text)
    return text


def get_answer(text: str) -> str:
    if text.startswith('/'):  # обработка команд
        for command in BOT_CONFIG['intents']['commands']:
            if text == command:
                return BOT_CONFIG['intents']['commands'][command]
    else:  # обработка простых сообщений
        text = clean(text)
        for intent in BOT_CONFIG['intents']:
            if intent == 'commands':
                continue
            for example in BOT_CONFIG['intents'][intent]['example']:
                if nltk.edit_distance(text, example)/max(len(text), len(example)) * 100 < 40:
                    # если различие между 2 словами менее, чем 40%, то пропускаем слово (может понадобится, если человек
                    # делает какую-то орфографическую ошибку в слове)
                    return BOT_CONFIG['intents'][intent]['answer']
            else:
                return BOT_CONFIG['default']


@bot.message_handler(content_types=['text'])
def work(message) -> None:
    """
    Main function which forces bot to work.
    :param message: text from user
    :return: None
    """
    reply: str = get_answer(message.text)
    if reply[0:8] == 'commands':
        if reply[9:] == 'help.py':
            with subprocess.Popen(['python', reply], stdout=subprocess.PIPE) as process:
                bot.send_message(message.from_user.id, process.stdout.read().decode(encoding='utf-8'))
        else:
            bot.send_message(message.from_user.id, 'Введите город, где будет проводится поиск.')
            bot.register_next_step_handler(message, get_city, reply)
    else:
        bot.send_message(message.from_user.id, reply)


def get_city(message, path: str):
    global max_hotel_count
    if message.text.isalpha():
        command = shlex.split(f'python {path}')
        with subprocess.run(command, stdout=subprocess.PIPE, input=message.text.encode()) as process:
            result = process.stdout.read().decode(encoding='utf-8')
        result = json.loads(result)
        max_hotel_count = len(result['suggestions'][1]['entities'])
        bot.send_message(message.from_user.id, 'Введите количество отелей, которые необходимо вывести в результате.')
        bot.register_next_step_handler(message, get_hotel_count, path)
    else:
        bot.send_message(message.from_user.id, 'В ответе не должно быть символов, кроме символов текста.')


def get_hotel_count(message, path: str):
    global hotel_count
    try:
        hotel_count = int(message.text)
    except TypeError:
        bot.send_message(message.from_user.id, 'В ответе должно быть только число.')
    else:
        global max_hotel_count
        if hotel_count > max_hotel_count:
            bot.send_message(message.from_user.id,
                             f'Вы запрашиваете слишком много отелей.\nКол-во отелей, которое будет '
                             f'выведено: {max_hotel_count}')
        else:
            max_hotel_count = hotel_count
            print(f'Кол-во отелей, которое будет выведено: {max_hotel_count}')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)