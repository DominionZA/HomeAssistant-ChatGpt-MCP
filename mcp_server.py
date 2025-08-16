#!/usr/bin/env python3
import asyncio
import json
from typing import Any, Sequence
import requests
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Configuration from environment variables
import os

HA_URL = os.getenv("HA_URL", "http://homeassistant.local:8123")
TOKEN = os.getenv("HA_TOKEN")

if not TOKEN:
    raise ValueError("HA_TOKEN environment variable is required")

app = Server("homeassistant-chatgpt")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="send_ha_command",
            description="Send a command to ChatGPT in Home Assistant to control devices",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The command to send to ChatGPT (e.g., 'Turn on the living room lights')"
                    }
                },
                "required": ["message"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Handle tool calls."""
    if name != "send_ha_command":
        raise ValueError(f"Unknown tool: {name}")
    
    if not arguments or "message" not in arguments:
        raise ValueError("Missing required argument: message")
    
    message = arguments["message"]
    
    try:
        # Send command to Home Assistant ChatGPT
        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        data = {
            "text": message,
            "agent_id": "conversation.chatgpt"
        }
        
        response = requests.post(f"{HA_URL}/api/services/conversation/process", 
                               headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Format response
            if isinstance(result, list) and len(result) > 0:
                # Check if any devices were affected
                affected_devices = []
                for item in result:
                    if item.get('entity_id', '').startswith('light.') or \
                       item.get('entity_id', '').startswith('switch.') or \
                       item.get('entity_id', '').startswith('climate.'):
                        device_name = item.get('attributes', {}).get('friendly_name', item.get('entity_id'))
                        state = item.get('state')
                        affected_devices.append(f"{device_name}: {state}")
                
                if affected_devices:
                    response_text = f"✓ Command sent to ChatGPT: '{message}'\n\nDevices affected:\n" + "\n".join(f"• {device}" for device in affected_devices)
                else:
                    response_text = f"✓ Command sent to ChatGPT: '{message}'\nNo device changes detected in response."
            else:
                response_text = f"✓ Command sent to ChatGPT: '{message}'\nCommand processed successfully."
            
            return [TextContent(type="text", text=response_text)]
        else:
            error_msg = f"✗ Failed to send command to Home Assistant\nStatus: {response.status_code}\nError: {response.text}"
            return [TextContent(type="text", text=error_msg)]
            
    except requests.exceptions.Timeout:
        return [TextContent(type="text", text="✗ Timeout connecting to Home Assistant")]
    except requests.exceptions.ConnectionError:
        return [TextContent(type="text", text="✗ Cannot connect to Home Assistant - check if it's running")]
    except Exception as e:
        return [TextContent(type="text", text=f"✗ Error: {str(e)}")]

async def main():
    # Run the server using stdin/stdout streams
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="homeassistant-chatgpt",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def run_server():
    """Entry point for console script."""
    asyncio.run(main())

if __name__ == "__main__":
    run_server()