import requests
import re
import json
import telebot
import nltk
from telebot import TeleBot
from typing import List, Dict, Union, Optional
from dotenv import load_dotenv
import os
# импорт скриптов
from commands.help import help
from commands.lowprice import get_city
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


@bot.message_handler(commands=['help', 'start'])
def main_commands_catcher(message):
    result = ''
    if message.text == '/start':
        result = 'Добро пожаловать!\nЯ помощник по подбору лучшего предложения в среде отелей для Вас\n'
    result += help(BOT_CONFIG)
    bot.send_message(message.from_user.id, result)


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def additional_commands_catcher(message):
    globals()[message.text[1:]](message)


@bot.message_handler(content_types=['text'])
def text_catcher(message) -> None:
    """
    Main function which forces bot to work.
    :param message: text from user
    :return: None
    """
    reply: str = get_answer(message.text)
    bot.send_message(message.from_user.id, reply)


def lowprice(message):
    bot.send_message(message.from_user.id, 'Введите город, где будет проводится поиск.')
    bot.register_next_step_handler(message, get_city, message.text[1:])


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)