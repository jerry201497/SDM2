
from rdflib import Graph, Namespace, RDF, XSD, URIRef, Literal
import json

with open("data_science_papers.json", "r", encoding="utf-8") as f:
    data = json.load(f)["data"]

EX = Namespace("http://example.org/research/")
g = Graph()
g.bind("ex", EX)

def uri(name):
    return URIRef(EX + name.replace(" ", "_").replace("/", "_"))

for paper in data:
    pid = paper.get("paperId") or paper["title"].replace(" ", "_")
    paper_uri = uri(f"paper_{pid}")
    g.add((paper_uri, RDF.type, EX.Paper))
    g.add((paper_uri, EX.hasAbstract, Literal(paper.get("abstract", ""), datatype=XSD.string)))
    g.add((paper_uri, EX.heldInYear, Literal(str(paper.get("year", "")), datatype=XSD.gYear)))

    for topic in paper.get("topics", []):
        topic_uri = uri(f"topic_{topic}")
        g.add((topic_uri, RDF.type, EX.Topic))
        g.add((paper_uri, EX.hasKeyword, topic_uri))

    if paper.get("synthetic"):
        conf_uri = uri(f"conference_{paper['venue']}")
        edition_uri = uri(f"edition_{paper['edition']}")
        g.add((conf_uri, RDF.type, EX.Conference))
        g.add((edition_uri, RDF.type, EX.Edition))
        g.add((conf_uri, EX.hasEdition, edition_uri))
        g.add((edition_uri, EX.heldInYear, Literal(str(paper["year"]), datatype=XSD.gYear)))
        g.add((paper_uri, EX.publishedInProceedings, edition_uri))
    else:
        journal_uri = uri(f"journal_{paper['venue']}")
        g.add((journal_uri, RDF.type, EX.Journal))
        if paper.get("volume"):
            volume_uri = uri(f"volume_{paper['volume']}")
            g.add((volume_uri, RDF.type, EX.Volume))
            g.add((journal_uri, EX.hasVolume, volume_uri))
        g.add((paper_uri, EX.publishedInJournal, journal_uri))

    for author in paper.get("authors", []):
        if "name" not in author:
            continue
        author_uri = uri(f"author_{author['name']}")
        g.add((author_uri, RDF.type, EX.Author))
        g.add((paper_uri, EX.hasAuthor, author_uri))
        if author["name"] == paper.get("correspondingAuthor"):
            g.add((paper_uri, EX.correspondingAuthor, author_uri))

    for ref in paper.get("references", []):
        if ref.get("paperId"):
            cited_uri = uri(f"paper_{ref['paperId']}")
            g.add((paper_uri, EX.cites, cited_uri))

    for reviewer in paper.get("reviewers", []):
        reviewer_uri = uri(f"reviewer_{reviewer}")
        g.add((reviewer_uri, RDF.type, EX.Author))
        review_uri = uri(f"review_{pid}_{reviewer}")
        g.add((review_uri, RDF.type, EX.Review))
        g.add((review_uri, EX.assignedReviewer, reviewer_uri))
        g.add((paper_uri, EX.hasReview, review_uri))

g.serialize(destination="abox_research.rdf", format="xml")
