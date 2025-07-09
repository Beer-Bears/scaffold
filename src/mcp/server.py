from fastmcp import FastMCP

from src.generator.generator import get_node_information

mcp = FastMCP(
    name="Scaffold MCP Server",
    instructions="""
    This is a mock MCP server for the Scaffold project. It provides a mock LLM endpoint for testing and integration.
    Use the `mock_llm` tool to simulate LLM responses.
    """,
)


@mcp.tool
def node_information(
    node_name: str,
) -> dict:
    """
    Find node with relevant name and return information (code, relationships).
    """
    return {
        "response": get_node_information(node_name),
    }
