from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from models.post_model import Post
import uuid
from icecream import ic

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
    },
        {
        "title": "Nike Pegasus 39",
        "content": "A cool looking shoe for running",
        "published": True,
        "rating": 5,
        "id": 123
    }
    ]

def find_post(id): 
    for i in my_posts: 
        if i["id"] == id:
            return i

def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"} #FastAPI directly converts this into JSON 


@app.get("/posts")
async def get_posts():
    return {"data": my_posts} #FastAPI directly converts this into JSON 

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(new_post: Post):
    new_post = new_post.model_dump()
    new_post['id'] = str(uuid.uuid4())
    my_posts.append(new_post)


    return {"message": new_post} #FastAPI directly converts this into JSON 


@app.get("/posts/{id}")
async def get_posts(id:str,response: Response):
    post = find_post(id)
    if post is None: 

        # *FIRST WAY TO SETTING RESPONSE 
        # response.status_code = 404
        # return {"msg": f"Post with id {id} not found"}

        # *2nd WAY OF SETTING RESPONSE
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"msg": f"Post with id {id} not found"}

        #* 3rd and BEST WAY OF SETTING RESPONSE
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
        #* 4th way is described in the delete method
        # in which we set the status code in the decorator
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    post_index = find_index_post(id)

    if post_index is None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    my_posts.pop(post_index)
    # return {"msg": "post was successfully deleted"} 
    # * We donot need to return anything on delete request, even if we return anything, FastAPI will not return anything by default 
    # So there is no point of writing return statement on delete request


@app.put("/posts/{id}")
def update_post(id, post:Post):
    print(post)
    post_index = find_index_post(id)

    if post_index is None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post_dict = post.model_dump()
    post_dict['id'] = id 
    ic(post_dict)
    my_posts[post_index] = post_dict

    return {"message" : my_posts[post_index]}