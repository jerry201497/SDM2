import requests
import xml.etree.ElementTree as ET
import random
import time
from neo4j_connection import conn

def fetch_dblp_data(author_query, max_papers=10):
    url = f"https://dblp.org/search/publ/api?q={author_query}&h={max_papers}&format=xml"
    response = requests.get(url)
    root = ET.fromstring(response.text)
    return root.findall(".//hit/info")

def generate_mock_data(title):
    keywords = ["graph processing", "data quality", "property graph", "knowledge graph", "query optimization"]
    return {
        "abstract": f"This is a mock abstract for the paper: {title}.",
        "keywords": random.sample(keywords, k=random.randint(1, 3))
    }

def insert_dblp_paper(paper_id, title, year, authors, venue, citations=[]):
    mock = generate_mock_data(title)
    query = """
    MERGE (p:Paper {paperId: $paperId})
    SET p.title = $title, p.abstract = $abstract, p.year = $year
    MERGE (v:Venue {name: $venue})
    MERGE (p)-[:PUBLISHED_IN]->(v)
    WITH p
    UNWIND $keywords AS kw
        MERGE (t:Topic {keyword: kw})
        MERGE (p)-[:HAS_TOPIC]->(t)
    """
    params = {
        "paperId": paper_id,
        "title": title,
        "abstract": mock["abstract"],
        "year": year,
        "venue": venue,
        "keywords": mock["keywords"]
    }
    conn.query(query, params)

    for i, author_name in enumerate(authors):
        is_corr = (i == 0)
        conn.query("""
        MERGE (a:Author {name: $name})
        MERGE (p:Paper {paperId: $paperId})
        MERGE (p)-[:AUTHORED_BY {corresponding: $isCorresponding}]->(a)
        """, {"name": author_name, "paperId": paper_id, "isCorresponding": is_corr})

    for cited_id in citations:
        conn.query("""
        MERGE (p1:Paper {paperId: $source})
        MERGE (p2:Paper {paperId: $target})
        MERGE (p1)-[:CITES]->(p2)
        """, {"source": paper_id, "target": cited_id})

def assign_reviewers(paper_id, all_authors):
    potential_reviewers = list(all_authors)
    random.shuffle(potential_reviewers)
    assigned = []
    for reviewer in potential_reviewers:
        if reviewer not in paper_authors[paper_id] and len(assigned) < 3:
            review_id = f"review_{paper_id}_{reviewer.replace(' ', '_')}"
            conn.query("""
            MERGE (r:Review {reviewId: $reviewId})
            SET r.score = $score
            MERGE (p:Paper {paperId: $paperId})
            MERGE (rev:Author {name: $reviewer})
            MERGE (r)-[:REVIEWS]->(p)
            MERGE (r)-[:BY]->(rev)
            """, {
                "reviewId": review_id,
                "score": random.randint(1, 10),
                "paperId": paper_id,
                "reviewer": reviewer
            })
            assigned.append(reviewer)

if __name__ == "__main__":
    query = "knowledge graph"
    max_papers = 15
    entries = fetch_dblp_data(query, max_papers)
    paper_authors = {}
    print(f"Fetched {len(entries)} papers from DBLP")

    for idx, entry in enumerate(entries):
        title = entry.findtext("title")
        year = entry.findtext("year", default="2020")
        venue = entry.findtext("venue", default="Unknown Venue")
        authors = [a.text for a in entry.findall("authors/author")]
        paper_id = f"dblp_{idx}_{random.randint(1000,9999)}"
        insert_dblp_paper(paper_id, title, year, authors, venue)
        paper_authors[paper_id] = authors

    all_authors = {author for authors in paper_authors.values() for author in authors}
    for paper_id in paper_authors:
        assign_reviewers(paper_id, all_authors)

    conn.close()
    print("DBLP data added with authors, reviews, topics, and citations.")
