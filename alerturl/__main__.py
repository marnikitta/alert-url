from typing import Annotated
import uvicorn

import typer
from fastapi import FastAPI, Query

from alerturl.dotenv import load_dotenv
from alerturl.systemd import try_notify_systemd
from alerturl.telegram import Bot

app = FastAPI()
bot: Bot


@app.on_event("startup")
def notify():
    try_notify_systemd()


@app.get("/info")
def info(message: Annotated[str, Query(alias="m")]):
    bot.send_message(bot.owner_id, "[INFO] " + message, silent=True)


@app.get("/warn")
def warning(message: Annotated[str, Query(alias="m")]):
    bot.send_message(bot.owner_id, "[WARN] " + message, silent=False)


@app.get("/error")
def error(message: Annotated[str, Query(alias="m")]):
    bot.send_message(bot.owner_id, "[ERROR] " + message, silent=False)


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
