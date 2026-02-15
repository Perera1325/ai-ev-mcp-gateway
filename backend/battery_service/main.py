from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

@app.get("/battery-status")
def get_battery_status():
    charge = random.uniform(30, 100)

    return {
        "battery_charge_percent": round(charge, 2),
        "timestamp": datetime.now()
    }
