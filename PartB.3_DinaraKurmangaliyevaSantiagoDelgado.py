from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def calculate_impact_factors(self):
        query = """
        WITH 2021 AS target_year
        MATCH (citing:Paper)-[:CITES]->(cited:Paper)-[:PUBLISHED_IN]->(v:Venue)
        WHERE citing.year = target_year AND cited.year IN [target_year - 1, target_year - 2]
        WITH v.name AS venue, COUNT(cited) AS total_citations, target_year

        MATCH (p:Paper)-[:PUBLISHED_IN]->(v2:Venue)
        WHERE p.year IN [target_year - 1, target_year - 2]
        AND v2.name = venue  // make sure we're counting papers for the same venue
        WITH venue, total_citations, COUNT(p) AS recent_papers
        WHERE recent_papers > 0
        RETURN venue, ROUND(total_citations * 1.0 / recent_papers, 2) AS impact_factor
        ORDER BY impact_factor DESC


        """
        with self.driver.session() as session:
            result = session.run(query)
            print("\n Impact Factor by Venue:\n")
            for record in result:
                print(f"{record['venue']}: {record['impact_factor']}")

if __name__ == "__main__":
    uri = "bolt://localhost:7690"
    user = "neo4j"
    password = "123456789"  # Replace with your actual Neo4j password

    db = Neo4jConnector(uri, user, password)
    db.calculate_impact_factors()
    db.close()
