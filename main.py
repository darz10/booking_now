from asyncio import get_event_loop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import create_db
from settings import settings
from accounts.views import user, authorization
from institutions.views import (
    place, 
    place_branch, 
    country, 
    city, 
    address,
    user_place,
    table,
    reservation,
    media_file,
    place_media_file
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    app.settings = settings
    app.loop = get_event_loop()
    await create_db()


app.include_router(user.router)
app.include_router(authorization.router)
app.include_router(place.router)
app.include_router(place_branch.router)
app.include_router(country.router)
app.include_router(city.router)
app.include_router(address.router)
app.include_router(user_place.router)
app.include_router(table.router)
app.include_router(reservation.router)
app.include_router(media_file.router)
app.include_router(place_media_file.router)
