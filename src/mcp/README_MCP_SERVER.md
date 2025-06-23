# Testing the Scaffold MCP Server

After building and running the container (or starting the app via your main entrypoint), you can test the MCP server as follows:

---

## Testing with AI Tools

### Using Roo Code (VS Code Extension, recommended)

1. Install the "Roo Code" extension from the VS Code Marketplace.
2. Open the Roo Code extension sidebar in VS Code.
3. Click the settings (gear) icon and set the MCP server URL to:
   ```
   http://localhost:8000/mcp
   ```
4. Use the Roo Code chat or tool interface to call the `mock_llm` tool. Example prompt:
   > Use the `mock_llm` tool with prompt: "Hello, Roo!"

### Using Cursor

1. Open Cursor and go to the AI integration settings.
2. Set the MCP server endpoint to:
   ```
   http://localhost:8000/mcp
   ```
3. Use the AI chat or tool interface to call the `mock_llm` tool.

---

## Example: Testing the Endpoint Directly

You can also test the endpoint with curl:

```bash
curl -X POST http://localhost:8000/mcp/tool/mock_llm -H "Content-Type: application/json" -d '{"prompt": "Test prompt", "context": {}, "options": {}}'
```

Expected response:

```json
{
  "response": "Mock response to: Test prompt",
  "tokens_used": 2,
  "model": "mock-llm-v1",
  "meta": {
    "version": "0.1.0",
    "source": "mock-llm-endpoint",
    "processing_time_ms": 100
  }
}
```

---

You can now use this server with Roo Code, Cursor, or any MCP-compatible client for development and testing.
