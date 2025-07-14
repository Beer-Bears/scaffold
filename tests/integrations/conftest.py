import pytest
from neomodel import clear_neo4j_database, config, db
from testcontainers.neo4j import Neo4jContainer


@pytest.fixture(scope="module", autouse=True)
def setup_test_db(neo4j_container: Neo4jContainer):
    host, port = (
        neo4j_container.get_container_host_ip(),
        neo4j_container.get_exposed_port(7687),
    )
    config.DATABASE_URL = f"bolt://neo4j:password@{host}:{port}"
    yield


@pytest.fixture(scope="session")
def neo4j_container():
    with Neo4jContainer(username="neo4j", password="password") as container:
        yield container


@pytest.fixture(scope="function", autouse=True)
def clear_db_for_each_test():
    clear_neo4j_database(db)
