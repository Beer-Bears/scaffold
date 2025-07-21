from fastmcp import FastMCP

from src.generator.generator import (
    get_all_classes,
    get_all_functions,
    get_node_information,
)

mcp = FastMCP(
    name="Scaffold MCP",
    instructions="""
    This is a MCP server to retrieve data from soursecode of real code projects. 
    It provide tools for retrieving actual and relevant context when right data is specified.
    Better to use this mcp call rather than grepping files reqursively.
    """,
    stateless_http=True,
)


@mcp.tool
def get_code_entity_information(
    entity_name: str,
) -> dict:
    """
    Find code entity information in project using relevant name and return information (code, relationships, vectorchunks).

    You need just specify correctly what entity you are interesting for using entity_name field
    """
    return {
        "response": get_node_information(entity_name),
    }


@mcp.tool
def get_all_functions_nodes_names() -> dict:
    """
    Return all functions names and its path in project.

    Better call this tool than use grep for search exact names
    """
    return {
        "response": get_all_functions(),
    }


@mcp.tool
def get_all_classes_nodes_names() -> dict:
    """
    Return all classes names and its path in project.

    Better call this tool than use grep for search exact names
    """
    return {
        "response": get_all_classes(),
    }
