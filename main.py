from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello"} 



@app.get("/greet/{name}")
async def greetings(name:str):
    return {"message": f"Hello {name}"} 



@app.get("/greet-query-param/")
async def greetings_query(name:str):
    return {"message": f"Hello {name}"} 