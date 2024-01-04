from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"} #FastAPI directly converts this into JSON 


@app.get("/posts")
async def get_posts():
    return {"data": "This is your post"} #FastAPI directly converts this into JSON 

@app.post("/createposts")
async def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message": "successfully created post"} #FastAPI directly converts this into JSON 