from fastapi import FastAPI
import requests
import urllib3
import logging

# Disable SSL warnings (self-signed certificate from WSO2)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

# ===============================
# WSO2 GATEWAY ENDPOINTS
# ===============================

SOLAR_URL = "https://localhost:8243/solar/1.0.0/solar-status"
BATTERY_URL = "https://localhost:8243/battery/1.0.0/battery-status"
GRID_URL = "https://localhost:8243/grid/1.0.0/grid-load"

# ===============================
# ACCESS TOKEN (YOUR TOKEN)
# ===============================

ACCESS_TOKEN = "eyJ4NXQiOiJNekF6TVRGak9EUTFNRE5qT1RVMVpEQTROR1E1TURrell6RTNNV0k0TW1SbFpHVTNZelpqWWprNFpHUmtNMlJoTW1Jd01qQXhZekpsTUdKak5qZG1OdyIsImtpZCI6Ik16QXpNVEZqT0RRMU1ETmpPVFUxWkRBNE5HUTVNRGt6WXpFM01XSTRNbVJsWkdVM1l6WmpZams0WkdSa00yUmhNbUl3TWpBeFl6SmxNR0pqTmpkbU53X1JTMjU2IiwidHlwIjoiYXQrand0IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI3MDE0Yjg1Ny0zNmZjLTRiZmMtODY0OS0zM2QyOWM3ZTU0MTEiLCJhdXQiOiJBUFBMSUNBVElPTiIsImF1ZCI6IlpYOEE5R2d6YmwwQ2Z2cVpIY0hyaXczd2VUOGEiLCJuYmYiOjE3NzExNzA4MDQsImF6cCI6IlpYOEE5R2d6YmwwQ2Z2cVpIY0hyaXczd2VUOGEiLCJzY29wZSI6ImRlZmF1bHQiLCJpc3MiOiJodHRwczovL2xvY2FsaG9zdDo5NDQzL29hdXRoMi90b2tlbiIsImV4cCI6MTc3MTE3NDQwNCwiaWF0IjoxNzcxMTcwODA0LCJqdGkiOiIxZmRiMGMxNC02ZmIxLTRiN2UtYmMyMS02YzNlNzIzOTZiMTgiLCJjbGllbnRfaWQiOiJaWDhBOUdnemJsMENmdnFaSGNIcml3M3dlVDhhIn0.Hb7BxM16e0yFwVEbNPtHiBBnakteIXDvNAv9Eb7paDlrdvO7alWQc1KhjJ4K3J9Bio7ttatEMmmUm1_rXMjRHzLyrbkiWGXeBserbqKj1-e_f7X_sV2Ly_KxR8JT7Q-fFZR1jfYoma99wc85jIItLlLFWMWUlVI2wilYhA3HkxTQdcw0qf7LieW-bwmz8-DAuE7-BxdAJY3YOXlRY1TDrPJXVT4_r89tVmRdn9irw98Y5y-U_n5Fm7WBbav5c049jeGoZXH29xbYZnB9P-2RPeze_KCWtoQosap22ZyWYXx25BBryFvjismoDmsPdQ4GAPBKjSEDlVi6Dbyfhrg0MA"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# ===============================
# LOGGING CONFIGURATION
# ===============================

logging.basicConfig(level=logging.INFO)

# ===============================
# AI OPTIMIZATION ENDPOINT
# ===============================

@app.get("/optimize-charging")
def optimize_charging():
    try:
        solar_response = requests.get(SOLAR_URL, headers=HEADERS, verify=False)
        battery_response = requests.get(BATTERY_URL, headers=HEADERS, verify=False)
        grid_response = requests.get(GRID_URL, headers=HEADERS, verify=False)

        # Check for errors
        if (
            solar_response.status_code != 200 or
            battery_response.status_code != 200 or
            grid_response.status_code != 200
        ):
            return {
                "error": "Gateway call failed",
                "solar_status": solar_response.status_code,
                "battery_status": battery_response.status_code,
                "grid_status": grid_response.status_code,
                "solar_response": solar_response.text,
                "battery_response": battery_response.text,
                "grid_response": grid_response.text
            }

        solar = solar_response.json()
        battery = battery_response.json()
        grid = grid_response.json()

        solar_output = solar.get("solar_output_kW", 0)
        battery_level = battery.get("battery_charge_percent", 0)
        grid_load = grid.get("grid_load_percent", 0)

        # ===============================
        # DECISION LOGIC
        # ===============================

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

        # Logging
        logging.info(f"Solar: {solar_output}")
        logging.info(f"Battery: {battery_level}")
        logging.info(f"Grid: {grid_load}")
        logging.info(f"Decision: {decision}")

        return {
            "solar_output_kW": solar_output,
            "battery_level_percent": battery_level,
            "grid_load_percent": grid_load,
            "charging_mode": decision,
            "charging_power_kW": charging_power
        }

    except Exception as e:
        return {
            "error": "Exception occurred",
            "message": str(e)
        }
