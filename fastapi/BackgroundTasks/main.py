from fastapi import FastAPI
from fastapi import BackgroundTasks
from time import sleep

app = FastAPI()

def my_longrunning_background_function(status: str):
    sleep(5)
    print(f"\n\n\n---\nAll done, status {status}\n---\n\n\n")

@app.get("/")
async def hello(background_tasks: BackgroundTasks):
    background_tasks.add_task(my_longrunning_background_function, status="my status")
    return {"message": "Hello World"}

