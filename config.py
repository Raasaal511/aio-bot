import os

from dotenv import load_dotenv

load_dotenv()


class BotSettings:
    TOKEN: str = "8620064890:AAFz62P0EUX1vCV4Wd7uSk1y_q2gRf1VF6g"
    PAYMENT_TOKEN: str = "1744374395:TEST:d2a91f796d7659a4e1c3"

bot_settings = BotSettings()


class MapConfig:
    WEATHER_API_KEY = "52103fc8-df14-42d5-be09-40c5aface46b"
    GEOCODE_API_KEY = "98afc61d-d922-4d9f-9040-55f99f99e2b7"
    headers = {'X-Yandex-Weather-Key': WEATHER_API_KEY}
    weather_url = "https://api.weather.yandex.ru/v2/forecast"
    geocode_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={GEOCODE_API_KEY}"

map_config = MapConfig()
