from fastapi import FastAPI
from fastapi import Request
from time import sleep

app = FastAPI()

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    response = await call_next(request)
    # sleep(5)
    print("I executed")
    return response

@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.get("/goodbye")
async def goodbye():
    return {"message": "Goodbye World"}

