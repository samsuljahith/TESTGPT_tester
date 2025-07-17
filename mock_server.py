# mock_server.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/rockets/{id}")
def get_rocket(id: int):
    return {"id": id, "name": "Falcon", "price": 2999} 