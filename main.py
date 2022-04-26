from asyncio import get_event_loop
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import settings

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    app.state.settings = settings
    app.state.loop = get_event_loop()
