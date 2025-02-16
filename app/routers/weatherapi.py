import httpx
import asyncio
from ..config import settings
from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter()


WEATHER_API_URL=f"{settings.weather_api_url}"
WEATHER_API_KEY=f"{settings.weather_api_KEY}"

@router.get("/weather/{city}")
async def get_weather(city: str):
    params = {
    "q": f"{city}",
    "appid": WEATHER_API_KEY,
    "units": "metric"
    }
    async with httpx.AsyncClient() as client: # AsyncClient client of httpx.
        try:
            response = await client.get(WEATHER_API_URL, params=params)
            print(response.status_code)  # Should be 200
            return response.json() 
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error fetching weather data")