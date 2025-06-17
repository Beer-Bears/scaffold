import pytest
from httpx import AsyncClient
from src.mcp.mcp import LLMRequest

@pytest.mark.asyncio
async def test_context_endpoint(client: AsyncClient):
    response = await client.get("/mcp/context")
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "metadata" in data
    
    project = data["data"]["project"]
    assert project["name"] == "Scaffold"
    assert project["description"] == "Specialized RAG system for large codebases"
    
    databases = project["databases"]
    assert "postgresql" in databases
    assert "neo4j" in databases
    
    metadata = data["metadata"]
    assert metadata["version"] == "0.1.0"
    assert metadata["source"] == "mock-endpoint"

@pytest.mark.asyncio
async def test_context_response_structure(client: AsyncClient):
    response = await client.get("/mcp/context")
    data = response.json()
    
    required_fields = [
        "data.project.name",
        "data.project.description",
        "data.project.databases.postgresql.type",
        "data.project.databases.neo4j.type",
    ]
    
    for field in required_fields:
        keys = field.split(".")
        current = data
        for key in keys:
            assert key in current
            current = current[key]

@pytest.mark.asyncio
async def test_llm_endpoint(client: AsyncClient):
    request_data = LLMRequest(
        prompt="What is the purpose of the Scaffold project?",
        context={"user": "tester"},
        options={"max_tokens": 100}
    )
    
    response = await client.post("/mcp/llm", json=request_data.model_dump())
    assert response.status_code == 200
    
    data = response.json()
    assert "data" in data
    assert "meta" in data
    
    llm_response = data["data"]
    assert "response" in llm_response
    assert "tokens_used" in llm_response
    assert "model" in llm_response
    
    assert isinstance(llm_response["response"], str)
    assert isinstance(llm_response["tokens_used"], int)
    assert isinstance(llm_response["model"], str)
    
    meta = data["meta"]
    assert "version" in meta
    assert "source" in meta
    assert "processing_time_ms" in meta