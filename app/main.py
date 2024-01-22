from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from post_model import Post
import uuid
from icecream import ic
import psycopg2
from psycopg2.extras import RealDictCursor
from decouple import config

app = FastAPI()

try:
    conn = psycopg2.connect(host= 'localhost' , dbname= "fastapi", 
                        user='postgres', port=5432, password=config("DB_PASSWORD"), 
                        cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successfull")
except Exception as ex:
    raise Exception(ex)

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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts} #FastAPI directly converts this into JSON 


# create post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(post: Post):
    # * %s protects us from SQL injections
        # We can write query like INSERT INTO posts (title, content, published) VALUSE ({title}, {content}, {published})
        # using the f string but some user can pass the SQL statements directly into these variables 
        # to prevent this we use %s statement to sanitize the values coming from the user's end and then pass to the query
    
    # RETURNING * will return the newly created object
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                   (post.title, post.content, post.published) ) 
    new_post = cursor.fetchone()

    # it will store information in the database
    conn.commit()

    return {"message": new_post} #FastAPI directly converts this into JSON 


@app.get("/posts/{id}")
async def get_posts(id:int,response: Response):
    # We cannot use VALUES keyword in the select statement, this is against SQL syntax. 
    # VALUES keyword is specifically designed for the INSERT Statements
    cursor.execute("SELECT * FROM posts WHERE id = (%s)", (id,))
    post = cursor.fetchone()
    if not post: 

        # *FIRST WAY TO SETTING RESPONSE 
        # response.status_code = 404
        # return {"msg": f"Post with id {id} not found"}

        # *2nd WAY OF SETTING RESPONSE
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"msg": f"Post with id {id} not found"}

        #* 3rd OF SETTING RESPONSE
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
        #* 4th way is described in the delete method
        # in which we set the status code in the decorator
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id = (%s) RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # return {"msg": "post was successfully deleted"} 
    # * We donot need to return anything on delete request, even if we return anything, FastAPI will not return anything by default 
    # So there is no point of writing return statement on delete request


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("UPDATE posts SET title=%s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"message" : updated_post}