import asyncio
import requests
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import tg_bot_token, open_weather_token


bot = Bot(token=tg_bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Москва"), types.KeyboardButton(text="Санкт-Петербург")],
        [types.KeyboardButton(text="Маями"), types.KeyboardButton(text="Ялта")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Здраствуй! В каком городе ты бы хотел узнать погоду?", reply_markup=keyboard)


@dp.message()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"👨‍💻{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}👨‍💻\n"
                            f"Погода в городе {city}\nТемпература: {int(cur_weather)}°\n{wd}\n"
                            f"💧 Влажность: {humidity}%\n💥 Давление: {pressure} мм.рт.ст\n🌬 Ветер: {wind} м/с\n"
                            f"🌅 Восход солнца: {sunrise_timestamp}\n🌄 Закат солнца: {sunset_timestamp}\n☀ Продолжительность дня: {length_of_the_day}\n"
                            )

    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
