from fastapi import FastAPI
from lib.dummy import dummy_function
app = FastAPI()

@app.get("/dummy")
def dummy(name: str):
    return dummy_function(name)