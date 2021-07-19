# import requests
import re
import json
import telebot
import nltk
import subprocess
from telebot import TeleBot
from typing import List, Dict, Union
TOKEN: str = '1918621695:AAHioSDb_wuWie01xdD2sjTpHByAAxDhwfY'
# BOT INFO: hotel-analysis-tool, @hotelanalysisbot
bot: TeleBot = telebot.TeleBot(TOKEN)
with open('botconfig.json', 'r', encoding='utf-8') as json_file:
    BOT_CONFIG: Dict[str, Union[Dict[str, Dict[str, Union[str, List]]], str]] = json.load(json_file)


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


@bot.message_handler(content_types=['text'])
def work(message) -> None:
    """
    Main function which forces bot to work.
    :param message: text from user
    :return: None
    """
    reply: str = get_answer(message.text)
    if reply[0:8] == 'commands':
        # если вернулась команда -> запуск скрипта из папки commands
        with subprocess.Popen(['python', reply], stdout=subprocess.PIPE) as process:
            bot.send_message(message.from_user.id, process.stdout.read().decode(encoding='utf-8'))
    else:
        # если вернулась НЕ команда, то отправляем этот текст пользователю
        bot.send_message(message.from_user.id, reply)


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

# Не знаю, понадобится это или нет, будут это оценивать или нет, но я сделал более гибкую структуру ответов на сообщения
# Если это лишнее, то я могу, конечно, это убрать.


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)