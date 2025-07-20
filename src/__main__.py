import threading

from src.core.config import get_settings
from src.core.indexer import run_indexing
from src.core.watcher import start_watcher
from src.mcp.server import mcp

settings = get_settings()

PROJECT_PATH = "./codebase/"

if __name__ == "__main__":
    run_indexing()

    w = threading.Thread(target=start_watcher, daemon=True)
    w.start()

    mcp.run(**settings.mcp_server.model_dump())
