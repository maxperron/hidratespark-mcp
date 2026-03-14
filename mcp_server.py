# /// script
# requires-python = ">=3.10"
# dependencies = ["fastmcp"]
# ///

import os
import json
import urllib.request
import urllib.error
from fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("HidrateSpark MCP")

# Configuration
API_URL = os.environ.get("HIDRATESPARK_API_URL", "http://localhost:3000/api")
API_KEY = os.environ.get("HIDRATESPARK_API_KEY")

def get_headers():
    if not API_KEY:
        raise ValueError("HIDRATESPARK_API_KEY environment variable is not set!")
    return {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

def make_request(url, method="GET", data=None):
    headers = get_headers()
    req_data = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        raise RuntimeError(f"HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")

@mcp.tool()
def get_daily_goal(date: str) -> str:
    """Get the hydration goal for a specific date (YYYY-MM-DD)."""
    try:
        return make_request(f"{API_URL}/goal?date={date}", method="GET")
    except Exception as e:
        return f"Error fetching daily goal: {e}"

@mcp.tool()
def update_daily_goal(date: str, goal: int) -> str:
    """Update the hydration goal (in ml) for a specific date (YYYY-MM-DD)."""
    try:
        payload = {"date": date, "goal": goal}
        return make_request(f"{API_URL}/goal", method="POST", data=payload)
    except Exception as e:
        return f"Error updating daily goal: {e}"

@mcp.tool()
def get_hydration_history(start_date: str, end_date: str = None, timezone_offset: float = 0.0) -> str:
    """
    Get hydration history (sips and manual entries).
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD). Defaults to start_date.
        timezone_offset: The offset from UTC in hours (e.g., -5.0 for EST).
    """
    try:
        if not end_date:
            end_date = start_date
        url = f"{API_URL}/get-history?start_date={start_date}&end_date={end_date}&timezone_offset={timezone_offset}"
        return make_request(url, method="GET")
    except Exception as e:
        return f"Error fetching hydration history: {e}"

if __name__ == "__main__":
    mcp.run()
