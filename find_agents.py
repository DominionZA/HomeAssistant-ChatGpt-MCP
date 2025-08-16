import requests
import os

HA_URL = os.getenv("HA_URL", "http://homeassistant.local:8123")
TOKEN = os.getenv("HA_TOKEN")

if not TOKEN:
    print("Error: HA_TOKEN environment variable is required")
    exit(1)

headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Get all conversation entities
response = requests.get(f"{HA_URL}/api/states", headers=headers)
if response.status_code == 200:
    states = response.json()
    conversation_agents = [state for state in states if state['entity_id'].startswith('conversation.')]
    
    print("Available conversation agents:")
    for agent in conversation_agents:
        entity_id = agent['entity_id']
        friendly_name = agent['attributes'].get('friendly_name', 'Unknown')
        print(f"  {entity_id} - {friendly_name}")
else:
    print(f"Error getting states: {response.status_code} - {response.text}")