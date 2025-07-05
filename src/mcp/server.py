from fastmcp import FastMCP

mcp = FastMCP(
    name="Scaffold MCP Server",
    instructions="""
    This is a mock MCP server for the Scaffold project. It provides a mock LLM endpoint for testing and integration.
    Use the `mock_llm` tool to simulate LLM responses.
    """,
)


@mcp.tool
def mock_llm(node_name: str) -> dict:
    """
    Mock LLM endpoint that simulates AI model responses.
    """
    return {
        "response": f"Node `{node_name}`",
        "path": "some/path.py",
        "used_in": "some/another.py",
        "docstring": f"{node_name} make API requests and write to DB",
    }
