from fastmcp import FastMCP
from typing import Optional, Dict

mcp = FastMCP(
    name="Scaffold MCP Server",
    instructions="""
    This is a mock MCP server for the Scaffold project. It provides a mock LLM endpoint for testing and integration.
    Use the `mock_llm` tool to simulate LLM responses.
    """
)

@mcp.tool
def mock_llm(prompt: str, context: Optional[Dict] = None, options: Optional[Dict] = None) -> dict:
    """
    Mock LLM endpoint that simulates AI model responses.
    """
    return {
        "response": f"Mock response to: {prompt}",
        "tokens_used": len(prompt.split()),
        "model": "mock-llm-v1",
        "meta": {
            "version": "0.1.0",
            "source": "mock-llm-endpoint",
            "processing_time_ms": 100
        }
    }

