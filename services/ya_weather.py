import asyncio
import aiohttp

from map_conf import map_config


async def get_coords(city: str):
    async with aiohttp.ClientSession() as session:
        params = {"geocode": city, "format": "json"}

        async with session.get(map_config.geocode_url, params=params) as resp:
            resp_json = await resp.json()
            response_geo =  resp_json["response"]
            geo_object_collection = response_geo["GeoObjectCollection"]
            feature = geo_object_collection["featureMember"]
            geo_object = feature[0]["GeoObject"]
            points = geo_object["Point"]
            lon, lat = points["pos"].split()
            return lat, lon


def get_daytime(fact: dict):
    daytime = fact["daytime"]
    if daytime == "n":
            daytime = "Ночь"
    if daytime == "e":
            daytime = "Вечер"
    if daytime == "d":
            daytime = "День"
    if daytime == "m":
            daytime = "Утро"
    return daytime


def get_season(fact: dict):
    season = fact["season"]
    if season == "autumn":
        season = "Осень"
    if season == "winter":
        season = "Зима"
    if season == "summer":
        season = "Лето"
    if season == "spring":
        season = "Весна"   
    return season


async def get_weather_to_day(city: str):
    async with aiohttp.ClientSession() as session:
        lat, lon = await get_coords(city=city)
        params = {"lat": lat, "lon": lon}
        async with session.get(map_config.weather_url, params=params,
                               headers=map_config.headers) as resp:
                resp_json = await resp.json()
                fact = resp_json["fact"]
                daytime = get_daytime(fact)
                season = get_season(fact)
                feels_like = f"Ощущается как {fact["feels_like"]}°C"
                temp = f"Температура {fact["temp"]}°C"
                weather_data = {
                     "daytime": daytime,
                     "season": season,
                     "feels_like": feels_like,
                     "temp": temp
                }
                return weather_data


asyncio.run(get_weather_to_day("Грозный"))