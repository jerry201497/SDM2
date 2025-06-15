from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "123456789"

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def query(self, query, parameters=None, return_result=True):
        with self._driver.session() as session:
            result = session.run(query, parameters)
            return result.data() if return_result else None

    def clear_database(self):
        self.query("MATCH (n) DETACH DELETE n", return_result=False)
        print("All nodes and relationships have been deleted.")

    def update_property(self, label, match_field, match_value, update_field, new_value):
        query = f"""
        MATCH (n:{label} {{{match_field}: $match_value}})
        SET n.{update_field} = $new_value
        RETURN n
        """
        params = {"match_value": match_value, "new_value": new_value}
        return self.query(query, params)

    def delete_node_by_property(self, label, property_key, property_value):
        query = f"""
        MATCH (n:{label} {{{property_key}: $value}})
        DETACH DELETE n
        """
        self.query(query, {"value": property_value}, return_result=False)
        print(f"Deleted node with {property_key} = {property_value} in label {label}")

    def get_all_nodes(self, label):
        query = f"MATCH (n:{label}) RETURN n"
        return self.query(query)

conn = Neo4jConnection(URI, USER, PASSWORD)