# /// script
# requires-python = ">=3.10"
# dependencies = ["fastmcp", "requests"]
# ///

import os
import requests
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

@mcp.tool()
def get_daily_goal(date: str) -> str:
    """Get the hydration goal for a specific date (YYYY-MM-DD)."""
    try:
        response = requests.get(f"{API_URL}/goal?date={date}", headers=get_headers())
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching daily goal: {e}"

@mcp.tool()
def update_daily_goal(date: str, goal: int) -> str:
    """Update the hydration goal (in ml) for a specific date (YYYY-MM-DD)."""
    try:
        payload = {"date": date, "goal": goal}
        response = requests.post(f"{API_URL}/goal", json=payload, headers=get_headers())
        response.raise_for_status()
        return response.text
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
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error fetching hydration history: {e}"

if __name__ == "__main__":
    mcp.run()
