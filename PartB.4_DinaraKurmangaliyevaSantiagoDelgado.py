from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def calculate_h_index(self):
        query = """
        MATCH (a:Author)<-[:AUTHORED_BY]-(p:Paper)
        OPTIONAL MATCH (p)<-[:CITES]-(citing:Paper)
        WITH a.name AS author, p, COUNT(citing) AS citations
        ORDER BY author, citations DESC
        WITH author, COLLECT(citations) AS citation_list
        RETURN author,
               REDUCE(h = 0, c IN citation_list | CASE WHEN c >= h + 1 THEN h + 1 ELSE h END) AS h_index
        ORDER BY h_index DESC
        """
        with self.driver.session() as session:
            result = session.run(query)
            print("\n H-Index per Author:\n")
            for record in result:
                print(f"{record['author']}: h-index = {record['h_index']}")

if __name__ == "__main__":
    uri = "bolt://localhost:7690"
    user = "neo4j"
    password = "123456789"  # Replace with your actual Neo4j password

    db = Neo4jConnector(uri, user, password)
    db.calculate_h_index()
    db.close()
