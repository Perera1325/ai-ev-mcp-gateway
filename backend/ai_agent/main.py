from fastapi import FastAPI
import requests
import urllib3
import logging
import os
from requests.auth import HTTPBasicAuth

# Disable SSL warnings (WSO2 self-signed certificate)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

# ==========================================
# CONFIGURATION
# ==========================================

# WSO2 Gateway Endpoints
SOLAR_URL = "https://localhost:8243/solar/1.0.0/solar-status"
BATTERY_URL = "https://localhost:8243/battery/1.0.0/battery-status"
GRID_URL = "https://localhost:8243/grid/1.0.0/grid-load"

# OAuth2 Token Endpoint
TOKEN_URL = "https://localhost:9443/oauth2/token"

# Environment Variables (Set in terminal)
CLIENT_ID = os.getenv("WSO2_CLIENT_ID")
CLIENT_SECRET = os.getenv("WSO2_CLIENT_SECRET")

# ==========================================
# LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================================
# TOKEN GENERATION FUNCTION
# ==========================================

def get_access_token():
    try:
        if not CLIENT_ID or not CLIENT_SECRET:
            logging.error("Client ID or Client Secret not set.")
            return None

        response = requests.post(
            TOKEN_URL,
            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
            verify=False
        )

        if response.status_code == 200:
            token = response.json().get("access_token")
            logging.info("Access token retrieved successfully.")
            return token
        else:
            logging.error(f"Token request failed: {response.text}")
            return None

    except Exception as e:
        logging.error(f"Token generation error: {str(e)}")
        return None

# ==========================================
# HEALTH CHECK ENDPOINT
# ==========================================

@app.get("/health")
def health_check():
    return {"status": "AI Smart EV Charging Orchestrator Running"}

# ==========================================
# AI CHARGING OPTIMIZATION
# ==========================================

@app.get("/optimize-charging")
def optimize_charging():
    try:
        token = get_access_token()

        if not token:
            return {"error": "Failed to retrieve access token"}

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Call Gateway APIs
        solar_response = requests.get(SOLAR_URL, headers=headers, verify=False)
        battery_response = requests.get(BATTERY_URL, headers=headers, verify=False)
        grid_response = requests.get(GRID_URL, headers=headers, verify=False)

        # Check for gateway errors
        if (
            solar_response.status_code != 200 or
            battery_response.status_code != 200 or
            grid_response.status_code != 200
        ):
            logging.error("Gateway call failed.")
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

        # ==========================================
        # DECISION LOGIC
        # ==========================================

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
        logging.info(f"Solar: {solar_output} kW")
        logging.info(f"Battery: {battery_level} %")
        logging.info(f"Grid: {grid_load} %")
        logging.info(f"Decision: {decision} ({charging_power} kW)")

        return {
            "solar_output_kW": solar_output,
            "battery_level_percent": battery_level,
            "grid_load_percent": grid_load,
            "charging_mode": decision,
            "charging_power_kW": charging_power
        }

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return {
            "error": "Exception occurred",
            "message": str(e)
        }
