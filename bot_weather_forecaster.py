import telebot
import requests
import json
import math


token = '7372464954:AAFsSPMnWf1eoJfgfsv-GNRg2wJ4W7QsVTA'
API_weather = 'afb89f2b6515034f82c2eb4130a3f9bd'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    '''Функция приветствия'''
    bot.send_message(message.chat.id, 'Привет, рад помочь тебе с погодой.'
                                      '\nНапиши название города, в котором требуется узнать погоду')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    '''Функция обрабатывает погоду в нужном городе и выводит в чат'''
    try:
        city = message.text.strip().lower()
        res = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid={API_weather}')
        data = json.loads(res.text)
        city_name = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        bot.send_message(message.chat.id, f"Погода в городе: {city_name}\nТемпература: {cur_temp}°C\n"
                                                f"Влажность: {humidity}%\nДавление: {math.ceil(pressure/1.33)} мм.рт.ст"
                                                f"\nВетер: {wind} м/с \nХорошего дня!")
    except:
        bot.send_message(message.chat.id, 'Проверьте название города и повторите попытку')


if __name__ == '__main__':
    bot.infinity_polling()