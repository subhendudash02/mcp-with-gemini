# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.tool()
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.tool()
def find_range(field_name: str, start: int, end: int):
    li = [{"Name": "Subhendu", "marks1": "41", "marks2": "32"},
          {"Name": "Subhendu2", "marks1": "100", "marks2": "56"},
          {"Name": "Subhendu3", "marks1": "70", "marks2": "35"}]
    
    """Find the range of a field in a list of dictionaries"""
    if field_name not in li[0]:
        return "Field not found"
    if start > end:
        return "Invalid range"
    count = 0
    for item in li:
        if field_name in item and start <= int(item[field_name]) <= end:
            count += 1
    return count

def register():
    mcp.run("stdio")

if __name__ == "__main__":
    register()