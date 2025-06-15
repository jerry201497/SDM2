from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def top_cited_papers_per_venue(self):
        query = """
        MATCH (p:Paper)-[:PUBLISHED_IN]->(v:Venue)
        OPTIONAL MATCH (p)<-[:CITES]-(citing:Paper)
        WITH v.name AS venue, p.title AS paper, COUNT(citing) AS citations
        WITH venue, paper, citations
        ORDER BY venue, citations DESC
        WITH venue, COLLECT({paper: paper, citations: citations})[0..3] AS top_papers
        UNWIND top_papers AS tp
        RETURN venue, tp.paper AS paper, tp.citations AS citations

        """

        with self.driver.session() as session:
            result = session.run(query)
            current_venue = None
            for record in result:
                venue = record["venue"]
                if venue != current_venue:
                    print(f"\n=== {venue} ===")
                    current_venue = venue
                print(f"• {record['paper']} ({record['citations']} citations)")

if __name__ == "__main__":
    uri = "bolt://localhost:7690"
    user = "neo4j"
    password = "123456789"  # Replace with your Neo4j password

    db = Neo4jConnector(uri, user, password)
    db.top_cited_papers_per_venue()
    db.close()
