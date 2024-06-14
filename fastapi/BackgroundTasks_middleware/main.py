from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi import Request
from time import sleep

app = FastAPI()

@app.middleware("http")
async def my_longrunning_background_function_middleware(request: Request, call_next):
    background_tasks = BackgroundTasks()
    background_tasks.add_task(my_longrunning_background_function, status="my status")
    response = await call_next(request)
    response.background = background_tasks
    return response

def my_longrunning_background_function(status: str):
    sleep(5)
    print(f"\n\n\n---\nAll done, status {status}\n---\n\n\n")

@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.get("/goodbye")
async def goodbye():
    return {"message": "Goodbye World"}

