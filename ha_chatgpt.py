#!/usr/bin/env python3
import requests
import json
import sys
import argparse
from typing import Optional

class HomeAssistantChatGPT:
    def __init__(self, ha_url: str, token: str):
        self.ha_url = ha_url.rstrip('/')
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def send_command(self, message: str, agent_id: str = "conversation.openai_conversation") -> Optional[dict]:
        """Send a command to ChatGPT via Home Assistant conversation API"""
        url = f"{self.ha_url}/api/services/conversation/process"
        
        payload = {
            "text": message,
            "conversation_id": None,
            "agent_id": agent_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending command: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test connection to Home Assistant"""
        try:
            response = requests.get(f"{self.ha_url}/api/", headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

def load_config() -> dict:
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config file not found. Please create config.json")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Send commands to ChatGPT in Home Assistant')
    parser.add_argument('message', help='Message to send to ChatGPT')
    parser.add_argument('--url', help='Home Assistant URL (overrides config)')
    parser.add_argument('--token', help='Home Assistant token (overrides config)')
    parser.add_argument('--agent', default='conversation.openai_conversation', 
                       help='Conversation agent ID')
    parser.add_argument('--test', action='store_true', help='Test connection only')
    
    args = parser.parse_args()
    
    # Load config or use command line args
    if args.url and args.token:
        ha_url = args.url
        token = args.token
    else:
        config = load_config()
        ha_url = args.url or config.get('ha_url', 'http://homeassistant.local:8123')
        token = args.token or config.get('token')
        
        if not token:
            print("Error: No token provided in config or command line")
            sys.exit(1)
    
    # Initialize client
    client = HomeAssistantChatGPT(ha_url, token)
    
    # Test connection if requested
    if args.test:
        if client.test_connection():
            print("✓ Connection to Home Assistant successful")
        else:
            print("✗ Failed to connect to Home Assistant")
        return
    
    # Send command
    print(f"Sending to ChatGPT: {args.message}")
    result = client.send_command(args.message, args.agent)
    
    if result:
        # Extract and display response
        response = result.get('response', {})
        speech = response.get('speech', {})
        plain_text = speech.get('plain', {}).get('speech', 'No response')
        print(f"Response: {plain_text}")
    else:
        print("Failed to get response")

if __name__ == "__main__":
    main()