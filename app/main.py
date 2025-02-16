from fastapi import FastAPI
from contextlib import asynccontextmanager
from redis import Redis
from redis import asyncio as aioredis
from .routers import weatherapi
import httpx
from .config import settings
import json

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize resources
    app.state.redis = aioredis.Redis(host="localhost", port=6379, decode_responses=True)
    app.state.http_client = httpx.AsyncClient()
    yield

    await app.state.http_client.aclose()
    await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(weatherapi.router)

@app.get("/weathers/")
async def get_weather():
    http_client = getattr(app.state, "http_client", None)
    if http_client is None:
        raise RuntimeError("HTTP client is not initialized")

    value = await app.state.redis.get("weathers")

    if value is None:
        response = await http_client.get(f"https://api.openweathermap.org/data/2.5/weather?q=Pune&appid={settings.weather_api_KEY}&units=metric")
        value = response.json()
        data_str = json.dumps(value)
        app.state.redis.set("weathers", data_str, ex=600)

    else:
        value = json.loads(value)

    return value