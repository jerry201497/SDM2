
from rdflib import Graph, Namespace, RDF, RDFS, XSD

EX = Namespace("http://example.org/research/")
g = Graph()
g.bind("ex", EX)

classes = [
    "Paper", "Author", "Conference", "Workshop", "Journal", "Proceedings",
    "Edition", "Volume", "Review", "Reviewer", "Topic", "City"
]
for cls in classes:
    g.add((EX[cls], RDF.type, RDFS.Class))

object_properties = {
    "hasAuthor": ("Paper", "Author"),
    "correspondingAuthor": ("Paper", "Author"),
    "publishedInProceedings": ("Paper", "Edition"),
    "publishedInJournal": ("Paper", "Journal"),
    "hasVolume": ("Journal", "Volume"),
    "hasEdition": ("Conference", "Edition"),
    "heldInCity": ("Edition", "City"),
    "cites": ("Paper", "Paper"),
    "hasReview": ("Paper", "Review"),
    "assignedReviewer": ("Review", "Reviewer"),
    "hasKeyword": ("Paper", "Topic")
}

for prop, (domain, range_) in object_properties.items():
    g.add((EX[prop], RDF.type, RDF.Property))
    g.add((EX[prop], RDFS.domain, EX[domain]))
    g.add((EX[prop], RDFS.range, EX[range_]))

g.add((EX["heldInYear"], RDF.type, RDF.Property))
g.add((EX["heldInYear"], RDFS.domain, EX["Edition"]))
g.add((EX["heldInYear"], RDFS.range, XSD.gYear))

g.add((EX["hasAbstract"], RDF.type, RDF.Property))
g.add((EX["hasAbstract"], RDFS.domain, EX["Paper"]))
g.add((EX["hasAbstract"], RDFS.range, XSD.string))

g.serialize(destination="tbox_research.rdfs", format="xml")
