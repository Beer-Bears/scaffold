### Overview
<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/scaffold-logo.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/scaffold-logo.png" alt="Scaffold Banner" style="width:85%;height:100%"/></a>
</h1>
<p align="center">
  <a href="https://github.com/Beer-Bears/scaffold"><img alt="GitHub" src="https://img.shields.io/badge/Scaffold-grey.svg?logo=github"></a>
  <a href="https://github.com/Beer-Bears/scaffold/actions/workflows/tests.yml"><img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/Beer-Bears/scaffold/tests.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Beer-Bears/scaffold/actions/workflows/compose-check.yaml"><img alt="Docker CI" src="https://img.shields.io/github/actions/workflow/status/Beer-Bears/scaffold/compose-check.yaml?branch=main&label=Docker%20CI"></a>
  <a href="https://github.com/Beer-Bears/scaffold/releases"><img alt="Latest Release" src="https://img.shields.io/github/v/release/Beer-Bears/scaffold"></a>
  <a href="https://github.com/Beer-Bears/scaffold/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Beer-Bears/scaffold"></a>
</p>

Welcome to the official Scaffold Model Context Protocol (MCP) server. Scaffold is a specialized Retrieval-Augmented Generation (RAG) system designed to provide deep, structural understanding of large codebases to LLMs and AI agents. It transforms your source code into a living knowledge graph, allowing for precise, context-aware interactions that go far beyond simple file retrieval.

This server enables MCP clients like Cursor to interface directly with the Scaffold knowledge graph, allowing them to effectively construct, maintain, and reason about complex software projects.

### Table of Contents

-   [Features](#features)
-   [Setup and Quickstart](#setup-and-quickstart)
-   [Configuration Explained](#configuration-explained)
-   [Available Tools](#available-tools)
-   [Usage Examples](#usage-examples)
-   [Troubleshooting](#troubleshooting)
-   [Contributing](#contributing)

### Features

-   **Graph-Based RAG:** Represents your codebase as an interconnected graph of files, classes, and functions, capturing structural relationships.
-   **Living Knowledge Base:** Keeps the AI's understanding synchronized with your code's structure.
-   **Eliminate Context Blindness:** Provides AI agents with project-specific architecture and logic, reducing the need for manual context feeding.
-   **Precise Context Injection:** Delivers targeted information about code entities, including their source, documentation, and relationships.
-   **Hybrid Search:** Combines graph-based traversal with vector search for comprehensive context retrieval.

### Setup and Quickstart

**Important:** Scaffold is a multi-service application. Before configuring your MCP client, you must have its database dependencies (Neo4j and ChromaDB) running and accessible to Docker. The following steps will guide you through the complete setup.

#### Step 1: Run Database Dependencies

You must start Neo4j and ChromaDB containers on a shared Docker network so the Scaffold container can connect to them.

1.  **Create a Docker Network:**
    ```bash
    docker network create scaffold-net
    ```

2.  **Run Neo4j:**
    ```bash
    docker run -d \
      --name scaffold-neo4j \
      --network scaffold-net \
      --restart unless-stopped \
      -p 7474:7474 -p 7687:7687 \
      -v neo4j_data:/data \
      -e NEO4J_AUTH="neo4j/password" \
      neo4j:5
    ```
    *This starts Neo4j with default user `neo4j` and password `password`.*

3.  **Run ChromaDB:**
    ```bash
    docker run -d \
      --name scaffold-chromadb \
      --network scaffold-net \
      --restart unless-stopped \
      -v chroma_data:/data \
      chromadb/chroma:1.0.13
    ```

#### Step 2: Configure Your MCP Client

Now, open your MCP client's configuration file (e.g., `mcp.json` in Cursor) and add the following server configuration. **You must replace the placeholder values (`<...>`) with your actual setup details.**

```json
{
  "mcpServers": {
    "Scaffold": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "--name", "scaffold-mcp",
        "--network", "scaffold-net",
        "-p", "8000:8080",
        "-v", "${PROJECT_PATH}:/app/codebase",
        "-e", "CHROMA_SERVER_HOST=${CHROMA_SERVER_HOST}",
        "-e", "CHROMA_SERVER_PORT=${CHROMA_SERVER_PORT}",
        "-e", "CHROMA_COLLECTION_NAME=${CHROMA_COLLECTION_NAME}",
        "-e", "NEO4J_USER=${NEO4J_USER}",
        "-e", "NEO4J_PASSWORD=${NEO4J_PASSWORD}",
        "-e", "NEO4J_URI=${NEO4J_URI}",
        "-t",
        "ghcr.io/beer-bears/scaffold:latest"
      ],
      "env": {
        "CHROMA_SERVER_HOST": "scaffold-chromadb",
        "CHROMA_SERVER_PORT": "8000",
        "CHROMA_COLLECTION_NAME": "scaffold_data",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_URI": "bolt://neo4j:password@scaffold-neo4j:7687",
        "PROJECT_PATH": "<ABSOLUTE_PATH_TO_YOUR_CODEBASE>"
      }
    }
  }
}
```
### Configuration Explained

The `env` block in the JSON is where you customize the server for your environment.

| Variable                  | Description                                                                                                                              | Example Value                                |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------- |
| `CHROMA_SERVER_HOST`      | The hostname of the ChromaDB container. If you followed Step 1, this is its container name.                                              | `scaffold-chromadb`                          |
| `CHROMA_SERVER_PORT`      | The internal port the ChromaDB container is listening on.                                                                                | `8000`                                       |
| `CHROMA_COLLECTION_NAME`  | The name of the collection to store vector embeddings.                                                                                   | `scaffold_data`                              |
| `NEO4J_USER`              | The username for the Neo4j database.                                                                                                     | `neo4j`                                      |
| `NEO4J_PASSWORD`          | The password for the Neo4j database.                                                                                                     | `password`                                   |
| `NEO4J_URI`               | The Bolt connection URI for Neo4j, using the container name as the host.                                                                 | `bolt://neo4j:password@scaffold-neo4j:7687`  |
| `PROJECT_PATH`            | **Crucial:** The absolute path to the source code you want to analyze on your local machine (the host).                                  | `/Users/me/projects/my-python-app`           |

### Available Tools

-   `get_code_entity_information(entity_name: str)`
    -   Finds a code entity (file, class, or function) by its name.
    -   Returns a rich context block including its source code, docstrings, structural relationships (e.g., "defines method X", "uses class Y"), and relevant vector chunks from the codebase.

### Usage Examples

You can now ask your AI agent to use the Scaffold tool with prompts like:

-   "Use the Scaffold tool to tell me about the `PaymentService` class."
-   "Find the source code and relationships for the `save_graph_to_db` function using Scaffold."
-   "What does the `FileNode` class do and what other methods use it? Use the `get_code_entity_information` tool."

### Troubleshooting

-   **Error: Container exits immediately or "Connection Refused".**
    This is the most common issue and almost always means the Scaffold container cannot connect to its database dependencies.
    1.  **Check Databases:** Ensure the `scaffold-neo4j` and `scaffold-chromadb` containers are running (`docker ps`).
    2.  **Check Network:** Verify that all three containers (the two databases and `scaffold-mcp`) are on the same Docker network (`scaffold-net`). The `docker` command in the `args` must include `--network scaffold-net`.
    3.  **Check Credentials:** Double-check that the user, password, and hostnames in the `env` block match the running database containers.

-   **Error: "File not found" or path-related issues inside the container.**
    This is likely due to an incorrect `PROJECT_PATH`. The value must be the **absolute path** to your code on your host machine. Relative paths (like `.` or `~/`) may not work correctly depending on your MCP client.

### Contributing

Scaffold is an open-source project and we welcome contributions. Please visit the [official GitHub repository](https://github.com/Beer-Bears/scaffold) to open an issue for bug reports, suggest features, or submit a pull request with your enhancements.