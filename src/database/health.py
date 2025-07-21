from neomodel import db


def check_neo4j():
    try:
        results, _ = db.cypher_query("RETURN 1")
        print(f"Neo4j: {results[0][0] == 1}")
    except Exception as e:
        print(f"Neo4j healthcheck failed: {e}")
        return False
