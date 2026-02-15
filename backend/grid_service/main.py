from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

@app.get("/grid-load")
def get_grid_load():
    load = random.uniform(40, 95)

    return {
        "grid_load_percent": round(load, 2),
        "timestamp": datetime.now()
    }
