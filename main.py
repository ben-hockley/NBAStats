from fastapi import FastAPI # import FastAPI
import uvicorn # import uvicorn


app = FastAPI() # create an instance of FastAPI


@app.get("/") # path operator decorator
async def root(): # path operator function
    return {"message": "Hello World"}

@app.get("/items/{item_id}") # path operator decorator
async def read_item(item_id: int):
    return {"item_id": item_id}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)