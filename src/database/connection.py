from neomodel import config  # type: ignore[import-untyped]

from src.database.config import settings

# --- ChromaDB ---



# --- Neo4j ---
def init_neo4j():
    """
    call in main
    """
    config.DATABASE_URL = settings.neo4j_uri
