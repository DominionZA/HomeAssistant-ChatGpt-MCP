import requests

import os

HA_URL = os.getenv("HA_URL", "http://homeassistant.local:8123")
TOKEN = os.getenv("HA_TOKEN")

if not TOKEN:
    print("Error: HA_TOKEN environment variable is required")
    exit(1)

# Send command to ChatGPT
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
data = {
    "text": "Turn the Pad Mi Lamp on and to one of the following colors - red, orange, pink, blue, yellow or purple. Don't choose a color it is currently.",
    "agent_id": "conversation.chatgpt"
}

response = requests.post(f"{HA_URL}/api/services/conversation/process", headers=headers, json=data)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Response: {result}")
else:
    print(f"Error: {response.text}")