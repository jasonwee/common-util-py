from fastapi import FastAPI, BackgroundTasks
from pydantic import HttpUrl
import time
import httpx

app = FastAPI()

async def post_callback(url: str, payload: dict):
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

async def long_running_task(duration: int, callback_url: str):
    # Simulate a time-consuming operation
    time.sleep(duration)

    # Send the result to the callback URL
    result = {"status": "completed", "data": "result_data"}
    await post_callback(callback_url, result)

@app.post("/start_task")
async def start_long_running_task(background_tasks: BackgroundTasks, duration: int = 10, callback_url: str = "http://example.com/callback"):
    background_tasks.add_task(long_running_task, duration, callback_url)
    return {"message": "Task started! You'll receive a notification at the callback URL once it's complete."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info", reload=True, workers=1)
