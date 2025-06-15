import requests
import json
import time
import random
from collections import defaultdict

def fetch_data(query, total_results=100, page_size=20, retries=5, wait_time=5):
    url_base = "https://api.semanticscholar.org/graph/v1/paper/search"
    all_results = []

    for offset in range(0, total_results, page_size):
        url = f"{url_base}?query={query}&offset={offset}&limit={page_size}&fields=title,authors,venue,year,referenceCount,references,abstract"

        for attempt in range(retries):
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json().get("data", [])

                for paper in data:
                    # Skip if no authors or title
                    if not paper.get("authors") or not paper.get("title"):
                        continue

                    # Assign a corresponding author
                    authors = paper["authors"]
                    paper["correspondingAuthor"] = authors[0]["name"] if authors else None

                    # Assign reviewers (from other authors)
                    all_author_names = list({a["name"] for p in data for a in p.get("authors", [])})
                    paper_authors = {a["name"] for a in authors}
                    reviewer_pool = list(set(all_author_names) - paper_authors)
                    paper["reviewers"] = random.sample(reviewer_pool, min(3, len(reviewer_pool))) if reviewer_pool else []

                    # Synthetic fields
                    paper["topics"] = ["data science", "graph processing", "AI"]
                    paper["synthetic"] = False  # real data

                all_results.extend(data)
                print(f"Fetched {len(data)} results (offset {offset})")
                break

            elif response.status_code == 429:
                print(f"Rate limited. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2

            else:
                print(f"Error {response.status_code} at offset {offset}")
                break

    return all_results

# Simulated conference with editions and synthetic authors
def add_conference_community(papers, community_size=5, editions=5, base_year=2015, venue_name="GraphConf"):
    community_authors = [f"Author_{i}" for i in range(community_size)]

    for author in community_authors:
        for i in range(editions):
            year = base_year + i
            edition_id = f"{venue_name}_Edition_{year}"
            paper_id = f"{edition_id}_{author.replace(' ', '_')}"
            paper = {
                "paperId": paper_id,
                "title": f"{venue_name} Research by {author} ({year})",
                "year": year,
                "venue": venue_name,
                "volume": None,
                "edition": edition_id,
                "authors": [{"name": author}],
                "correspondingAuthor": author,
                "topics": ["graph processing", "graph theory"],
                "reviewers": random.sample([a for a in community_authors if a != author], k=3),
                "referenceCount": 0,
                "references": [],
                "abstract": f"Exploration of graph research by {author} in {year}.",
                "synthetic": True
            }
            papers.append(paper)

def assign_journal_volumes(papers):
    journal_volumes = defaultdict(set)
    for paper in papers:
        if paper.get("venue") and not paper.get("synthetic"):
            journal = paper["venue"]
            year = paper.get("year")
            paper["volume"] = f"{journal}_Volume_{year}"
            journal_volumes[journal].add(year)
    return journal_volumes

# Main execution
if __name__ == "__main__":
    query = "data science"
    papers = fetch_data(query, total_results=100)

    # Add synthetic conference community
    add_conference_community(papers, community_size=5, editions=5, base_year=2017, venue_name="GraphConf")

    # Add journal volume info
    assign_journal_volumes(papers)

    # Save JSON
    if papers:
        with open("data_science_papers.json", "w", encoding="utf-8") as f:
            json.dump({"data": papers}, f, indent=4)
        print(f"Saved {len(papers)} papers to 'data_science_papers.json'")
