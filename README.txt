
# Knowledge Graph Assignment

This submission contains all the required elements for the Knowledge Graph Lab Assignment, including ontology creation, data processing, SPARQL querying, KGE training, and exploitation.

---

##Contents

###RDF and Ontology
- `tbox_research.rdfs`: RDFS ontology for the research domain.
- `abox_research.rdf`: RDF ABOX instances based on extracted data.

###Python Scripts
- `extract_json.py`: Script used to extract and simulate research paper data.
- `tbox_generator.py`: Generates the RDFS ontology using RDFLib.
- `abox_research.py`: Generates RDF ABOX instances from JSON data.
- `PyKEEN.py`: Uses TransE model to compute and predict embeddings.
- `PyKEEN_Experiments.py`: Trains and evaluates 4 KGE models (TransE, TransH, ComplEx, DistMult) and compares performance.
- `PyKEEN_Exploitation.py`: Clusters author embeddings using KMeans and visualizes them with PCA.

###Documents
- `knowledge_graph_report.docx`: Main report with methodology, results, SPARQL queries, KGE explanations, and plots.

###Output Files
- `kge_author_clusters.png`: Visualization of clustered author embeddings.
- `kge_experiment_results.csv`: Evaluation results from different KGE models.
- `kge_results.txt`: Output from TransE-based embedding prediction.

---

##Tasks Covered
- TBOX and ABOX definition with RDFLib
- SPARQL querying and inference in GraphDB
- Knowledge Graph Embeddings with PyKEEN
- Model comparison and selection
- Exploitation of embeddings in clustering task

---

##Requirements
- Python 3.8+
- PyKEEN
- RDFLib
- scikit-learn
- matplotlib
- pandas

To install dependencies:
```bash
pip install pykeen rdflib pandas matplotlib scikit-learn
```

---

For any questions or additional runs, start with the script `PyKEEN.py` and use the TSV file `kge_triples.tsv` exported from GraphDB.

