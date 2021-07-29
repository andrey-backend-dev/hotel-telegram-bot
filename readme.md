<h1 align="center"> Памятка по использованию телеграм бота hotel-analysis-tool </h1>
<h2 align="center">Подготовка к использованию бота</h2><br>
Для начала работы необходимо выполнить установку необходимых для работы бота пакетов:

```
pip install -r requirements.txt
```

Бот запускаются командой из корневой папки проекта

```
python main.py
```

---

<h2 align="center">Общая информация.</h2><br>

Бот пользуется бесплатным API сайта hotels.com. <br>
Ссылка на API: https://rapidapi.com/apidojo/api/hotels4

Для использования бота существует 4 команды:
* /help
* /lowprice
* /highprice
* /bestdeal

Также бот может реагировать на различные приветствия и прощания.
К обработке текста бота добавлены 2 функции: очистка текста от различных символов, а также игнорирование орфографических ошибок.

<p align="center"><img src="https://cdn1.savepice.ru/uploads/2021/7/29/4c569d113e8c64e4be20b6f480666eb9-full.jpg" alt="text communication"></p>

<figure align="center">
   <figcaption>В случае, если бот не может понять, что пишет пользователь, он ему отвечает:</figcaption>
   <img src="https://cdn1.savepice.ru/uploads/2021/7/29/01d4924141a04616438f1e4efef7a40d-full.jpg" alt="dont understand">
</figure>

---

<h2 align="center">Описание работы команд.</h2>

<figure align="center">
   <figcaption><h3>/help</h3>Помогает пользователю узнать об общей функциональности бота в Telegram (выводит список команд).</figcaption>
   <img src="https://cdn1.savepice.ru/uploads/2021/7/29/89729ac58a8d08b9a1aaf6f6f7eca80b-full.jpg" alt="help command">
</figure>

<figure align="center"> 
   <figcaption><h3>/lowprice</h3>Позволяет пользователю найти отели в городе, указанным пользователем, по самым дешевым ценам.</figcaption>
   <img src="https://cdn1.savepice.ru/uploads/2021/7/29/2b5933ff0a3d2f7f9c4f53d5c1d9f8bc-full.jpg" alt="lowprice command">
</figure>

<figure align="center">
   <figcaption><h3>/highprice</h3>Позволяет пользователю найти отели в городе, указанным пользователем, по самым высоким ценам.</figcaption>
   <img src="https://cdn1.savepice.ru/uploads/2021/7/29/bd5e2919ffb3db6038c4f15474098f90-full.jpg" alt="highprice command">
</figure>

<figure align="center">
   <figcaption><h3>/bestdeal</h3>Позволяет пользователю найти отели в городе, указанным пользователем, с допольнительным фильтром по минимальной и максимальной: цене, расстоянию от центра.</figcaption>
   <img src="https://cdn1.savepice.ru/uploads/2021/7/29/06484ebbbcfd7f7161d163ea82ea2c61-full.jpg" alt="bestdeal command">
</figure>