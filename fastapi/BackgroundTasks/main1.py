import asyncio
import logging
from typing import Dict

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.background import BackgroundTasks

logging.basicConfig(format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = FastAPI()


class Item(BaseModel):
    amount: int


async def background_async(amount: int) -> None:
    logger.debug(f"sleeping {amount}s")
    await asyncio.sleep(amount)
    logger.debug(f"slept {amount}s")


@app.post("/backgroundasync")
async def sleepingtheback(
    item: Item, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    background_tasks.add_task(background_async, item.amount)
    return {"message": f"sleeping {item.amount} in the back"}


if __name__ == "__main__":
    uvicorn.run(app=app)

