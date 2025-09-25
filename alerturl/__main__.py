from typing import Annotated
from contextlib import asynccontextmanager
import uvicorn

import typer
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from alerturl.dotenv import load_dotenv
from alerturl.systemd import try_notify_systemd
from alerturl.telegram import Bot

bot: Bot


@asynccontextmanager
async def lifespan(_: FastAPI):
    try_notify_systemd()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/info")
def info(message: Annotated[str, Query(alias="m")]):
    bot.send_message(bot.owner_id, "[INFO] " + message, silent=True)


@app.get("/warn")
def warning(message: Annotated[str, Query(alias="m")]):
    bot.send_message(bot.owner_id, "[WARN] " + message, silent=False)


@app.get("/error")
def error(message: Annotated[str, Query(alias="m")]):
    bot.send_message(bot.owner_id, "[ERROR] " + message, silent=False)


@app.get("/")
def index():
    return FileResponse("static/index.html")


def main(
    bot_owner_id: Annotated[int, typer.Argument(envvar=["BOT_OWNER_ID"])],
    bot_token: Annotated[str, typer.Argument(envvar=["BOT_TOKEN"])],
    host: Annotated[str, typer.Argument()] = "localhost",
    port: Annotated[int, typer.Argument()] = 8003,
):
    global bot
    bot = Bot(owner_id=bot_owner_id, token=bot_token)
    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=1,
    )


if __name__ == "__main__":
    load_dotenv()
    typer.run(main)
