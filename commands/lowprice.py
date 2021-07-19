import requests
import telebot
from telebot import TeleBot
from typing import List, Dict, Union, Optional
from dotenv import load_dotenv
import os

url = "https://hotels4.p.rapidapi.com/locations/search"
headers = {
            'x-rapidapi-key': "25aa467c2fmsh0ea943a8f40746dp1e2ef1jsn43ca10d68680",
            'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }
querystring = {"query": None,
               "locale": "ru_RU"}

city = input()
querystring['query'] = city
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)


