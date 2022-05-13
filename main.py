from asyncio import get_event_loop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from settings import settings
from accounts.views import user, authorization

app = FastAPI()

db = database.BookingDataBase(settings.DB_CONNECT)

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
    app.db = db
    await db.get_asyncpg_pool()


app.include_router(user.router)
app.include_router(authorization.router)
