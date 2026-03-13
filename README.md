# HidrateSpark MCP Server

This is a local Model Context Protocol (MCP) server that connects AI assistants (like Gemini CLI, Claude Desktop, Cursor) directly to your HidrateSpark PWA backend.

It uses the `uv` package manager to automatically fetch dependencies and run the server without manual environment setup.

## Prerequisites

1. Install [`uv`](https://github.com/astral-sh/uv):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Get your `x-api-key` from the `user_integrations` table in your Supabase database.

## Using with Gemini CLI

1. Open (or create) your Gemini CLI MCP configuration file at `~/.gemini/mcp.json`.
2. Add the `hidratespark` server configuration to the `mcpServers` object:

```json
{
  "mcpServers": {
    "hidratespark": {
      "command": "uv",
      "args": [
        "run",
        "/absolute/path/to/hidratespark-mcp/mcp_server.py"
      ],
      "env": {
        "HIDRATESPARK_API_KEY": "your-api-key-here",
        "HIDRATESPARK_API_URL": "https://your-vercel-pwa.vercel.app/api"
      }
    }
  }
}
```

*Note: Replace `/absolute/path/to/hidratespark-mcp` with the actual path to this folder (e.g., `/Users/maximeperron/Documents/Antigravity/hidratespark-mcp/mcp_server.py`), and replace the URL with your production PWA URL. If testing locally, you can use `http://localhost:3000/api`.*

## Available Tools

The MCP exposes the following tools to the AI:
- `get_daily_goal`: Retrieve the hydration goal for a specific date.
- `update_daily_goal`: Update the daily goal for a specific date.
- `get_hydration_history`: Retrieve a user's hydration sips and manual entries over a specific date range.

## Development

To test the server manually in your terminal (without an LLM client):
```bash
HIDRATESPARK_API_KEY="your-key" uv run mcp_server.py
```
*(This will start the server listening on stdio, expecting JSON-RPC messages.)*
