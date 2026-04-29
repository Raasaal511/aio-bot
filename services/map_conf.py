class MapConfig:
    WEATHER_API_KEY = "52103fc8-df14-42d5-be09-40c5aface46b"
    GEOCODE_API_KEY = "98afc61d-d922-4d9f-9040-55f99f99e2b7"
    headers = {'X-Yandex-Weather-Key': WEATHER_API_KEY}
    weather_url = "https://api.weather.yandex.ru/v2/forecast"
    geocode_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={GEOCODE_API_KEY}"

map_config = MapConfig()