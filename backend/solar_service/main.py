from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

@app.get("/solar-status")
def get_solar_status():
    hour = datetime.now().hour
    
    if 6 <= hour <= 18:
        output = random.uniform(20, 100)  # kW
    else:
        output = 0

    return {
        "solar_output_kW": round(output, 2),
        "timestamp": datetime.now()
    }
