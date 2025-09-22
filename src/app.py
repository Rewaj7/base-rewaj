from fastapi import FastAPI
from lib.dummy import dummy_function
app = FastAPI()

@app.get("/analyze")
def analyze(name: str):
    return dummy_function(name)