import requests
import telebot
from telebot import TeleBot
from typing import List, Dict, Union, Optional
from dotenv import load_dotenv
from datetime import datetime
import os
import json
load_dotenv()
TOKEN: str = os.getenv('TOKEN')
bot: TeleBot = telebot.TeleBot(TOKEN)
headers = {
            'x-rapidapi-key': "25aa467c2fmsh0ea943a8f40746dp1e2ef1jsn43ca10d68680",
            'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }


def get_city(message, command: str):
    if message.text.isalpha():
        url = "https://hotels4.p.rapidapi.com/locations/search"
        querystring = {"query": message.text,
                       "locale": 'ru_RU'}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)
        destination_id = int(response['suggestions'][0]['entities'][0]['destinationId'])
        bot.send_message(message.from_user.id, 'Введите количество отелей, которые необходимо вывести в результате.')
        bot.register_next_step_handler(message, get_hotel_count, command, destination_id)
    else:
        bot.send_message(message.from_user.id, 'В ответе не должно быть символов, кроме символов текста.')


def get_hotel_count(message, command: str, destination_id: int):
    # условно пусть мы заселяемся на 1 ночь, максимальное кол-во отелей для вывода: 10
    today = datetime.today()
    max_hotel_count = 10
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"adults1": "1", "pageNumber": "1", "destinationId": destination_id, "pageSize": "25",
                   "checkOut": str(today)[0:10],
                   "checkIn": f'{today.year}-{today.month}-{today.day + 1}', "sortOrder": "PRICE", "currency": "RUB"}

    response = requests.request('GET', url=url, headers=headers, params=querystring)
    response = json.loads(response.text)
    try:
        user_hotel_count = int(message.text)
    except TypeError:
        bot.send_message(message.from_user.id, 'В ответе должно быть только число.')
    else:
        print('Доступное кол-во отелей:', max_hotel_count)
        if user_hotel_count > max_hotel_count:
            bot.send_message(message.from_user.id,
                             f'Вы запрашиваете слишком много отелей.\n'
                             f'Кол-во отелей, которое будет выведено: {max_hotel_count}')
        else:
            max_hotel_count = user_hotel_count
            bot.send_message(message.from_user.id, f'Хорошо!\n'
                                                   f'Кол-во отелей, которое будет выведено: {max_hotel_count}')
        lowprice_main(message, response, max_hotel_count)


def lowprice_main(message, response: Dict, hotel_count: int):
    """
    Main function of low price script.
    Sends a result to an user.
    :param message: message object from user
    :param response: response from hotels.com API
    :param hotel_count: num of hotels which will be sent to an user
    :return:
    """
    for hotel in range(hotel_count):
        name = f"Название отеля: {response['data']['body']['searchResults']['results'][hotel]['name']}"
        address = f"Адрес: {response['data']['body']['searchResults']['results'][hotel]['address']['streetAddress']}"
        distance_from_centre = f"Расстояние от центра: {response['data']['body']['searchResults']['results'][hotel]['landmarks'][0]['distance']}"
        price = f"Цена: {response['data']['body']['searchResults']['results'][hotel]['ratePlan']['price']['fullyBundledPricePerStay'][6:]}"
        answer = '\n'.join([name, address, distance_from_centre, price])
        bot.send_message(message.from_user.id, answer)


