import aiohttp
from config.settings import GOOGLE_API_KEY, GOOGLE_CSE_ID


async def search_image(query: str) -> str | None:
    """Поиск изображения через Google API"""
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "searchType": "image",
        "num": 1,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                return data["items"][0]["link"] if "items" in data else None
    except Exception as e:
        print(f"Google API error: {e}")
        return None
