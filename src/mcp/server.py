from fastapi import FastAPI
from .mcp import router
import uvicorn

app = FastAPI(title="Scaffold MCP Server")
app.include_router(router, prefix="/mcp")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)