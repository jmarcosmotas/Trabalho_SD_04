from fastapi import FastAPI
import math
import time
import os

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/")
def home():
    return {"pod": os.getenv("HOSTNAME")}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cpu")
def cpu(segundos: int = 10):

    inicio = time.time()

    while time.time() - inicio < segundos:
        for i in range(1000000):
            _ = math.sin(i) + math.cos(i) + math.sqrt(i + 1)

    return {
        "message": "Carga finalizada",
        "pod": os.getenv("HOSTNAME")
    }

@app.get("/crash")
def crash():
    os._exit(1)