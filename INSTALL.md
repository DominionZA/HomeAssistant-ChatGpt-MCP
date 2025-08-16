# Home Assistant ChatGPT MCP Server Installation

## Quick Install

1. **Install the MCP server globally:**
   ```bash
   pip install -e .
   ```

2. **Test the server:**
   ```bash
   homeassistant-chatgpt-mcp
   ```
   (It will wait for input - press Ctrl+C to exit)

## Add to Claude Desktop

Add this to your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "homeassistant-chatgpt": {
      "command": "homeassistant-chatgpt-mcp"
    }
  }
}
```

## Usage

Once installed and configured, you can use it in any MCP-compatible AI:

- "Turn my lamp blue"
- "Turn off all the lights" 
- "Set the thermostat to 72 degrees"
- "Turn the Pad Mi Lamp on and to one of the following colors - red, orange, pink, blue, yellow or purple. Don't choose a color it is currently."

The tool will send your command to ChatGPT in Home Assistant and return the results.

## Configuration

Currently hardcoded in `mcp_server.py`:
- HA_URL: http://homeassistant.local:8123
- TOKEN: [your token]

Edit these values in the source code if needed.