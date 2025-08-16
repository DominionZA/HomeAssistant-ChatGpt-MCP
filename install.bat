@echo off
echo Installing Home Assistant ChatGPT MCP Server...
pip install -e .
echo.
echo Installation complete!
echo.
echo To test, run: homeassistant-chatgpt-mcp
echo.
echo Add this to Claude Desktop config:
echo {
echo   "mcpServers": {
echo     "homeassistant-chatgpt": {
echo       "command": "homeassistant-chatgpt-mcp"
echo     }
echo   }
echo }
pause