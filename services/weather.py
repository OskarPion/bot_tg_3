import httpx
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

async def get_weather(city: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

        if response.status_code != 200 or "main" not in data:
            return "❌ Не удалось получить погоду. Проверь название города."

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"].capitalize()
        wind = data["wind"]["speed"]
        humidity = data["main"]["humidity"]

        return (
            f"📍 Погода в {city.title()}:\n"
            f"🌡 Температура: {temp}°C\n"
            f"🤔 Ощущается как: {feels_like}°C\n"
            f"💧 Влажность: {humidity}%\n"
            f"💨 Ветер: {wind} м/с\n"
            f"🌥 {description}"
        )
