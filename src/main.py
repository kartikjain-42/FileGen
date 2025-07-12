from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from actions.read_files import read_files
from actions.delete_file import delete_path
from actions.init_project import init_project, write_file

from schemas.project_structure import get_project_structure

mcp = FastMCP("filegen", enable_streaming=False, host="127.0.0.1", port=8000)

# Register tools
mcp.add_tool(read_files)
mcp.add_tool(init_project)
mcp.add_tool(write_file)
mcp.add_tool(delete_path)
mcp.add_tool(get_project_structure)

if __name__ == "__main__":
    # Initialize and run the server
    print("Server Started...")
    # mcp.run(transport="streamable-http")
    # mcp.run(transport="sse")
    mcp.run(transport="stdio")
