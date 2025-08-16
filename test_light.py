import requests

# Your settings - CHANGE THESE
HA_URL = "http://homeassistant.local:8123"
TOKEN = "YOUR_TOKEN_HERE"  # Get from HA profile page
LIGHT_NAME = "light.living_room"  # Change to your light entity

# Send command
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
data = {"entity_id": LIGHT_NAME}

response = requests.post(f"{HA_URL}/api/services/light/turn_on", headers=headers, json=data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("Light turned on!")
else:
    print(f"Error: {response.text}")