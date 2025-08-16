# Home Assistant ChatGPT MCP Server

A Model Context Protocol (MCP) server that allows AI assistants to send commands to ChatGPT in Home Assistant. Compatible with Claude Desktop, Cursor, and any MCP-enabled AI client.

## Features

- Send natural language commands to ChatGPT in Home Assistant
- Works with any MCP-compatible AI client
- Secure environment variable configuration
- Real-time device state feedback

## Prerequisites

- Home Assistant with OpenAI Conversation integration configured
- Python 3.8+
- Long-lived access token from Home Assistant

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DominionZA/HomeAssistant-ChatGpt-MCP.git
   cd HomeAssistant-ChatGpt-MCP
   ```

2. **Install the MCP server:**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   
   **Windows (PowerShell):**
   ```powershell
   $env:HA_TOKEN = "your_long_lived_access_token_here"
   $env:HA_URL = "http://homeassistant.local:8123"  # Optional, defaults to this
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   set HA_TOKEN=your_long_lived_access_token_here
   set HA_URL=http://homeassistant.local:8123
   ```
   
   **Linux/Mac:**
   ```bash
   export HA_TOKEN="your_long_lived_access_token_here"
   export HA_URL="http://homeassistant.local:8123"  # Optional
   ```

   To make environment variables permanent:
   - **Windows:** Add them to System Environment Variables
   - **Linux/Mac:** Add the export commands to your `~/.bashrc` or `~/.zshrc`

## Getting Your Home Assistant Token

1. Go to your Home Assistant web interface
2. Click on your profile (bottom left)
3. Scroll down to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Give it a name like "MCP Server"
6. Copy the token and use it as your `HA_TOKEN`

## Configuration for AI Clients

### Claude Desktop

Add this to your Claude Desktop config file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "homeassistant-chatgpt": {
      "command": "homeassistant-chatgpt-mcp",
      "env": {
        "HA_TOKEN": "your_long_lived_access_token_here",
        "HA_URL": "http://homeassistant.local:8123"
      }
    }
  }
}
```

### Cursor

Add this to your Cursor config file:

**Windows:** `%APPDATA%\Cursor\User\globalStorage\anysphere.cursor\settings\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "homeassistant-chatgpt": {
      "command": "homeassistant-chatgpt-mcp",
      "env": {
        "HA_TOKEN": "your_long_lived_access_token_here",
        "HA_URL": "http://homeassistant.local:8123"
      }
    }
  }
}
```

After adding the configuration, restart your AI client.

## Usage

Once configured, you can use natural language commands in your AI client:

- "Turn on the living room lights"
- "Set the bedroom lamp to blue"
- "Turn off all the lights"
- "Set the thermostat to 72 degrees"
- "Turn the Pad Mi Lamp on and to one of the following colors - red, orange, pink, blue, yellow or purple. Don't choose a color it is currently."

The MCP server will:
1. Send your command to ChatGPT in Home Assistant
2. Return success/failure status
3. Show which devices were affected

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HA_TOKEN` | **Yes** | None | Your Home Assistant long-lived access token |
| `HA_URL` | No | `http://homeassistant.local:8123` | Your Home Assistant URL |

## Testing

Test the MCP server directly:
```bash
homeassistant-chatgpt-mcp
```

If configured correctly, it will start and wait for input. Press Ctrl+C to exit.

## Troubleshooting

**"HA_TOKEN environment variable is required"**
- Make sure you've set the `HA_TOKEN` environment variable
- Restart your terminal/AI client after setting variables

**"Cannot connect to Home Assistant"**
- Check that Home Assistant is running
- Verify your `HA_URL` is correct
- Ensure your token has the right permissions

**"No response from ChatGPT"**
- Verify OpenAI Conversation integration is set up in Home Assistant
- Check that ChatGPT has access to control your devices

## Security

- Never commit your Home Assistant token to version control
- Use environment variables to keep credentials secure
- Regularly rotate your access tokens

## License

MIT License - see LICENSE file for details.