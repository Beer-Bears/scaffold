from pathlib import Path
import logging
import threading
import os

from src.core.config import get_settings
from src.core.indexer import run_full_indexing
from src.core.watcher import start_watcher
from src.mcp.server import mcp

logger = logging.getLogger(__name__)
settings = get_settings()
PROJECT_PATH = "./codebase/"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    abspath = os.path.abspath(PROJECT_PATH)
    run_full_indexing(Path(abspath))

    w = threading.Thread(target=start_watcher, args=(abspath,), daemon=True)
    w.start()

    mcp.run(**settings.mcp_server.model_dump())
