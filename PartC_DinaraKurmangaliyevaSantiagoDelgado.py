from neo4j import GraphDatabase

class ReviewerRecommender:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def step_c1_define_community(self):
        query = """
        MERGE (c:Community {name: "Database"})
        WITH c
        UNWIND ["data management", "indexing", "data modeling", "big data", 
               "data processing", "data storage", "data querying"] AS kw
        MERGE (t:Topic {keyword: kw})
        MERGE (c)-[:HAS_KEYWORD]->(t)
        """
        with self.driver.session() as session:
            session.run(query)
            print("Step C.1: Community and keywords linked.")

    def step_c1b_assign_db_topics_to_papers(self):
        query = """
        MATCH (t:Topic)
        WHERE t.keyword IN ["data management", "indexing", "data modeling", "big data",
                            "data processing", "data storage", "data querying"]
        WITH COLLECT(t) AS db_topics
        MATCH (p:Paper)
        WITH p, db_topics[toInteger(rand() * SIZE(db_topics))] AS topic
        MERGE (p)-[:HAS_TOPIC]->(topic)
        """
        with self.driver.session() as session:
            session.run(query)
            print("Step C.1b: Random DB topics assigned to papers.")

    def step_c2_identify_related_venues(self):
        query = """
        MATCH (c:Community {name: "Database"})-[:HAS_KEYWORD]->(t:Topic)
        WITH c, COLLECT(t) AS db_topics

        MATCH (v:Venue)<-[:PUBLISHED_IN]-(p:Paper)
        WITH v, db_topics, COLLECT(p) AS all_papers

        UNWIND all_papers AS paper
        OPTIONAL MATCH (paper)-[:HAS_TOPIC]->(topic)
        WITH v, SIZE(all_papers) AS total, 
             COUNT(DISTINCT CASE WHEN topic IN db_topics THEN paper END) AS db_related

        WHERE total > 0 AND toFloat(db_related) / total >= 0.9
        MATCH (c:Community {name: "Database"})
        MERGE (v)-[:RELATED_TO]->(c)
        """
        with self.driver.session() as session:
            session.run(query)
            print("Step C.2: Related venues identified.")

    def step_c3_find_top_papers(self):
        query = """
        MATCH (c:Community {name: "Database"})-[:HAS_KEYWORD]->(t:Topic)
        MATCH (src:Paper)-[:HAS_TOPIC]->(t)
        MATCH (src)-[:CITES]->(p:Paper)-[:PUBLISHED_IN]->(v:Venue)-[:RELATED_TO]->(c)
        WITH p, COUNT(src) AS db_citations
        ORDER BY db_citations DESC
        LIMIT 100
        SET p:TopPaper
        """
        with self.driver.session() as session:
            session.run(query)
            print("Step C.3: Top-100 database papers tagged.")

    def step_c4_tag_reviewers_and_gurus(self):
        query = """
        MATCH (a:Author)<-[:AUTHORED_BY]-(p:TopPaper)
        WITH a, COUNT(p) AS top_count
        SET a:Reviewer
        WITH a, top_count WHERE top_count >= 2
        SET a:Guru
        """
        with self.driver.session() as session:
            session.run(query)
            print("Step C.4: Reviewers and gurus tagged.")

if __name__ == "__main__":
    uri = "bolt://localhost:7690"
    user = "neo4j"
    password = "123456789"  # Replace with your actual password

    recommender = ReviewerRecommender(uri, user, password)

    recommender.step_c1_define_community()
    recommender.step_c1b_assign_db_topics_to_papers()
    recommender.step_c2_identify_related_venues()
    recommender.step_c3_find_top_papers()
    recommender.step_c4_tag_reviewers_and_gurus()

    recommender.close()