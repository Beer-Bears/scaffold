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

**Scaffold** is a specialized RAG (Retrieval-Augmented Generation) system designed to revolutionize how development teams interact with large codebases. Born from real-world frustrations with traditional documentation and AI-assisted development, Scaffold provides the structural foundation AI agents need to effectively construct, maintain, and repair complex software projects.

## The Challenge

Modern development teams face three critical problems:

1.  **Documentation Decay:** Maintaining accurate and up-to-date technical documentation requires unsustainable manual effort.
2.  **AI Context Blindness:** LLMs lack awareness of project-specific architecture and business logic, requiring inefficient manual context provisioning.
3.  **Knowledge Fragmentation:** Critical system understanding exists only in tribal knowledge that's lost when team members leave.

## Our Solution

Scaffold transforms your source code into a living knowledge graph stored in a graph database. This creates an intelligent context layer that:

-   Captures structural relationships between code entities.
-   Maintains both vector and graph representations of your codebase.
-   Enables precise context injection for LLMs and AI agents.
-   Supports construction, maintenance, and refactoring workflows.

> Like its physical namesake, Scaffold provides the temporary support structure needed to build something great - then disappears when the work is done.

---

## Getting Started

There are two primary ways to run Scaffold. Choose the one that best fits your needs.

<details>
<summary><strong>Option 1: Run with Pre-built Docker Image (Recommended for Users)</strong>

> This is the fastest method to get Scaffold running. It uses the official pre-built image from the GitHub Container Registry and does not require you to clone the source code repository. You only need to create two configuration files.

</summary>


#### 1. Prepare Your Project Directory
Create a new folder for your project setup.

```bash
mkdir my-scaffold-server
cd my-scaffold-server
```

#### 2. Create Configuration Files
In the `my-scaffold-server` directory, create the following two files.

**`docker-compose.yaml`:**
```yaml
services:
  scaffold-mcp:
    image: ghcr.io/beer-bears/scaffold:latest
    container_name: scaffold-mcp-prod
    env_file:
      - .env
    tty: true
    ports:
      - "8000:8080"
    depends_on:
      - neo4j
    volumes:
      - ./codebase:/app/codebase

  chromadb:
    image: chromadb/chroma:1.0.13
    container_name: scaffold-chromadb
    restart: unless-stopped
    volumes:
      - chroma_data:/data

  neo4j:
    image: neo4j:5
    container_name: scaffold-neo4j
    restart: unless-stopped
    environment:
      NEO4J_AUTH: "${NEO4J_USER:-neo4j}/${NEO4J_PASSWORD:-password}"
    volumes:
      - neo4j_data:/data
    ports:
      - "7474:7474"
      - "7687:7687"

volumes:
  chroma_data:
  neo4j_data:
```

**`.env`:**
```dotenv
# ChromaDB Settings
CHROMA_SERVER_HOST=chromadb
CHROMA_SERVER_PORT=8000
CHROMA_COLLECTION_NAME=scaffold_data

# Neo4j Credentials
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_URI=bolt://neo4j:password@neo4j:7687

# Absolute path to your codebase
PROJECT_PATH=<ABSOLUTE_PATH_TO_YOUR_CODEBASE>
```

#### 3. Run the Application
Start all services using Docker Compose.
```bash
docker-compose up -d
```
Scaffold will now start and begin analyzing the code of your codebase.

</details>

<details>
<summary><strong>Option 2: Build from Source (For Developers)</strong>

> This method is for developers who have cloned the repository and want to build the Docker image locally. This is ideal for contributing to Scaffold or making custom modifications, or just run all containers at once in self-hosting mode.

</summary>

#### 1. Set Up The Project
First, clone the repository and navigate into the project directory.
```bash
git clone https://github.com/Beer-Bears/scaffold.git
cd scaffold
```
Next, create your environment file from the example provided.
```bash
cp .env.example .env
```

#### 2. Add Your Codebase
Place the Python project you want to analyze into the `codebase` directory.
```bash
# Create the directory if it doesn't exist
mkdir -p codebase

# Copy your project files into it
cp -r /path/to/your/python/project/* ./codebase/
```
Alternatively, you can edit the `.env` file and set the `PROJECT_PATH` variable to the absolute path of your project on your host machine.

#### 3. Run the Application
Start the entire application stack using Docker Compose. The `--build` flag will compile your local source code into a new Docker image.
```bash
docker-compose up --build -d
```
</details>

### Interact with Scaffold

Once the containers are running (using either method), you can interact with the system.

#### A. Configure your MCP Client (e.g., Cursor)
Add the Scaffold server to your client's `mcp.json` file.
```json
{
  "mcpServers": {
    "scaffold-mcp": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

#### B. Explore the Knowledge Graph
Access the Neo4j web UI to visually explore the graph of your codebase. Use the credentials from your `.env` file (default: `neo4j` / `password`).
**URL:** [http://localhost:7474/](http://localhost:7474/)

#### C. Send a Direct API Request
You can also test the MCP endpoint directly using `curl`.
```bash
curl -N -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "get_code_entity_information",
      "arguments": {
        "entity_name": "MyClassName"
      }
    }
  }'
```


> You also can check out [mcp description](MCP_DESCRIPTION.md) and get docker cmd configuration

---

## How It Works

### High-Level Architecture
<details>
<summary><strong> View Architecture Schema</strong> </summary>
<div align="center" style="display: block; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/architecture.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/architecture.png" alt="Scaffold Architecture" style="width:100%;height:100%"/></a></div>
</details>

### Usecase & Interface Diagrams
<details>
<summary><strong> View More Diagrams</strong> </summary>

**Usecase Schema**
<div align="center" style="display: block; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/usecase-diagram.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/usecase-diagram.png" alt="Scaffold Usecase Diagram" style="width:100%;height:100%"/></a></div>

**Interfaces Schema**
<div align="center" style="display: block; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a href="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/interfaces-diagram.png"><img align="center" src="https://raw.githubusercontent.com/Beer-Bears/scaffold/main/docs/img/interfaces-diagram.png" alt="Scaffold Interfaces" style="width:100%;height:100%"/></a></div>

</details>



### Project Structure

```
.
├── docs
│   ├── img       # Static Images
│   └── research  # Research reports
└── src
    ├── core      # RAG Context Fetching Algorithms
    ├── database  # Graph/Vector Database Logic
    ├── generator # Abstract Tree Generator
    ├── mcp       # MCP Interface
    └── parsers   # AST Parcers
```

## FAQ

<details>
<summary><strong>What is RAG (Retrieval-Augmented Generation)?</strong></summary>

RAG (Retrieval-Augmented Generation) is a technique that enhances large language models (LLMs) by:

1.  **Retrieving** relevant information from external knowledge sources
2.  **Augmenting** the LLM's context with this retrieved information
3.  **Generating** more accurate, context-aware responses

Unlike traditional LLMs that rely solely on their training data, RAG systems access up-to-date project-specific information and reduce hallucinations by grounding responses in actual codebase context.
</details>

<details>
<summary><strong>How does Graph RAG work?</strong></summary>

Graph RAG extends traditional RAG by representing knowledge as interconnected entities in a graph database. This allows the system to understand and retrieve not just chunks of text, but also the structural relationships between them (e.g., this function `calls` another function, this class `inherits from` another class). This structural context is invaluable for complex software engineering tasks.
</details>

## Resources

-   [What is Retrieval-Augmented Generation (RAG)?](https://www.youtube.com/watch?v=T-D1OfcDW1M)
-   [GraphRAG vs. Traditional RAG: Higher Accuracy & Insight with LLM](https://www.youtube.com/watch?v=Aw7iQjKAX2k)
-   [What is MCP? Integrate AI Agents with Databases & APIs](https://youtu.be/eur8dUO9mvE?si=TzSu6l-6CvSklnFH)

## Contributing

Scaffold is an open-source project and we welcome contributions. Please visit the [official GitHub repository](https://github.com/Beer-Bears/scaffold) to open an issue for bug reports, suggest features, or submit a pull request with your enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.