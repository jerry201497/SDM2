from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def community_authors_per_venue(self):
        query = """
        MATCH (a:Author)<-[:AUTHORED_BY]-(p:Paper)-[:PUBLISHED_IN]->(v:Venue)
        WHERE p.year IS NOT NULL
        WITH a.name AS author, v.name AS venue, COLLECT(DISTINCT p.year) AS years
        WHERE SIZE(years) >= 4
        RETURN venue, COLLECT(author) AS community_authors
        ORDER BY venue
        """
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                venue = record["venue"]
                authors = record["community_authors"]
                print(f"\n=== {venue} ===")
                if authors:
                    for name in authors:
                        print(f"• {name}")
                else:
                    print("No community authors found.")

if __name__ == "__main__":
    uri = "bolt://localhost:7690"
    user = "neo4j"
    password = "123456789"  

    db = Neo4jConnector(uri, user, password)
    db.community_authors_per_venue()
    db.close()
