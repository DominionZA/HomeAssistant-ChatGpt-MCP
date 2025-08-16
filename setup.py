from setuptools import setup, find_packages

setup(
    name="homeassistant-chatgpt-mcp",
    version="0.1.0",
    description="MCP server for Home Assistant ChatGPT integration",
    py_modules=["mcp_server"],
    install_requires=[
        "mcp>=0.1.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "homeassistant-chatgpt-mcp=mcp_server:run_server",
        ],
    },
    python_requires=">=3.8",
)