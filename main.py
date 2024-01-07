from fastapi import FastAPI
from fastapi.params import Body
from models.post_model import Post
import uuid
app = FastAPI()



my_posts = [
    {
        "title": "Nike Pegasus 40",
        "content": "A advance generation shoe for running",
        "published": True,
        "rating": 5,
        "id": "bf50381a-9e8c-4b3c-9f66-259192ff424a"
    },
    {
        "title": "Nike Pegasus 39",
        "content": "A cool looking shoe for running",
        "published": True,
        "rating": 5,
        "id": "f2615b82-f2ff-4003-96f0-ef05eca94ce6"
    }
    ]

@app.get("/")
async def root():
    return {"message": "Hello World"} #FastAPI directly converts this into JSON 


@app.get("/posts")
async def get_posts():
    return {"data": my_posts} #FastAPI directly converts this into JSON 

@app.post("/posts")
# async def create_posts(payload: dict = Body(...)):
async def create_posts(new_post: Post):
    new_post = new_post.model_dump()
    new_post['id'] = str(uuid.uuid4())
    my_posts.append(new_post)


    return {"message": new_post} #FastAPI directly converts this into JSON 


@app.get("/posts/{id}")
async def get_posts():
    return {"data": my_posts}