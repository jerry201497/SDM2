import json
from neo4j_connection import conn

conn.clear_database()

# Load the JSON data
with open("data_science_papers.json", "r", encoding="utf-8") as file:
    papers_data = json.load(file)["data"]

def insert_paper_data(paper):
    query = """
    MERGE (p:Paper {title: $title})
    SET p.year = $year,
        p.abstract = $abstract,
        p.correspondingAuthor = $correspondingAuthor

    MERGE (v:Venue {name: $venue})
    MERGE (p)-[:PUBLISHED_IN]->(v)

    WITH p
    UNWIND $authors AS author
        MERGE (a:Author {name: author.name})
        MERGE (p)-[:AUTHORED_BY]->(a)

    WITH p
    UNWIND $topics AS topic
        MERGE (t:Topic {name: topic})
        MERGE (p)-[:HAS_TOPIC]->(t)

    WITH p
    UNWIND $reviewers AS reviewer
        MERGE (r:Reviewer:Author {name: reviewer})
        MERGE (r)-[:REVIEWED]->(p)
    """

    params = {
        "title": paper.get("title"),
        "year": paper.get("year"),
        "abstract": paper.get("abstract"),
        "correspondingAuthor": paper.get("correspondingAuthor"),
        "venue": paper.get("venue", "Unknown Venue"),
        "authors": paper.get("authors", []),
        "topics": paper.get("topics", []),
        "reviewers": paper.get("reviewers", [])
    }

    conn.query(query, parameters=params)

    # Add references as CITES relationships
    references = paper.get("references", [])
    for ref in references:
        if ref.get("paperId"):
            ref_query = """
            MERGE (target:Paper {title: $refTitle})
            MERGE (source:Paper {title: $sourceTitle})
            MERGE (source)-[:CITES]->(target)
            """
            conn.query(ref_query, parameters={
                "refTitle": ref.get("title", "Unknown Title"),
                "sourceTitle": paper.get("title")
            })

# Insert each paper into Neo4j
for paper in papers_data:
    try:
        insert_paper_data(paper)
        print(f"Inserted paper: {paper['title']}")
    except Exception as e:
        print(f"Failed to insert paper: {paper['title']}. Error: {e}")

# Close the connection
conn.close()
print("All data loaded and connection closed.")