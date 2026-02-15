from fastapi import FastAPI
import requests

app = FastAPI()

SOLAR_URL = "http://127.0.0.1:8001/solar-status"
BATTERY_URL = "http://127.0.0.1:8002/battery-status"
GRID_URL = "http://127.0.0.1:8003/grid-load"

@app.get("/optimize-charging")
def optimize_charging():
    try:
        solar = requests.get(SOLAR_URL).json()
        battery = requests.get(BATTERY_URL).json()
        grid = requests.get(GRID_URL).json()

        solar_output = solar["solar_output_kW"]
        battery_level = battery["battery_charge_percent"]
        grid_load = grid["grid_load_percent"]

        # Decision Logic
        if grid_load > 85:
            decision = "PAUSE_CHARGING"
            charging_power = 0
        elif solar_output > 60 and battery_level > 70:
            decision = "FAST_CHARGING"
            charging_power = 22
        elif solar_output > 30:
            decision = "NORMAL_CHARGING"
            charging_power = 11
        else:
            decision = "SLOW_CHARGING"
            charging_power = 5

        return {
            "solar_output_kW": solar_output,
            "battery_level_percent": battery_level,
            "grid_load_percent": grid_load,
            "charging_mode": decision,
            "charging_power_kW": charging_power
        }

    except Exception as e:
        return {"error": str(e)}
