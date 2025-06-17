from fastapi import APIRouter
from fastmcp import MCPResponse
from typing import Dict, Any
from pydantic import BaseModel
import time
from ..core.config import get_settings

settings = get_settings()

class LLMRequest(BaseModel):
    prompt: str
    context: Dict[str, Any] = {}
    options: Dict[str, Any] = {}

class LLMResponse(BaseModel):
    response: str
    tokens_used: int
    model: str

router = APIRouter()

@router.get("/context")
async def get_context() -> MCPResponse:
    """
    Provides real project context based on configuration
    """
    context = {
        "project": {
            "name": settings.project_name,
            "description": settings.project_description,
            "databases": {
                "postgresql": {
                    "type": "relational",
                    "purpose": "Storing project metadata",
                    "status": "active" if settings.postgres_enabled else "disabled"
                },
                "neo4j": {
                    "type": "graph",
                    "purpose": "Knowledge graph storage",
                    "status": "active" if settings.neo4j_enabled else "disabled"
                }
            }
        }
    }
    
    return MCPResponse(
        data=context,
        meta={
            "version": settings.version,
            "source": "context-endpoint",
            "environment": settings.environment
        }
    )

@router.post("/llm")
async def llm_endpoint(request: LLMRequest) -> MCPResponse:
    """
    Processes LLM requests with real token counting and response generation
    """
    start_time = time.time()
    
    # Simple token counting (words + punctuation)
    tokens = len(request.prompt.split()) + sum(1 for c in request.prompt if c in '.,!?;:')
    
    # Generate response based on prompt and context
    response = generate_llm_response(request.prompt, request.context, request.options)
    
    processing_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
    
    mock_response = LLMResponse(
        response=response,
        tokens_used=tokens,
        model=settings.llm_model
    )
    
    return MCPResponse(
        data=mock_response.model_dump(),
        meta={
            "version": settings.version,
            "source": "llm-endpoint",
            "processing_time_ms": processing_time,
            "model": settings.llm_model
        }
    )

def generate_llm_response(prompt: str, context: Dict[str, Any], options: Dict[str, Any]) -> str:
    """
    Generates a response based on the prompt and context
    """
    # Basic response generation logic
    if "purpose" in prompt.lower():
        return "Scaffold is a specialized RAG system designed for efficient codebase analysis and understanding."
    elif "database" in prompt.lower():
        return "The system uses PostgreSQL for metadata storage and Neo4j for knowledge graph representation."
    elif "features" in prompt.lower():
        return "Key features include code parsing, context fetching, and intelligent code generation."
    else:
        return f"Processed request: {prompt}. Context: {context}. Options: {options}"