# Knowledge Graph Assignment

This repository contains all required files for the SDM2 Knowledge Graph assignment.

## 📂 Structure

- `PyKEEN.py`: Main script to train a TransE model on the RDF triples.
- `PyKEEN_Exploitation.py`: Uses trained embeddings to find the closest author to a selected paper.
- `PyKEEN_Experiments.py`: Trains and compares multiple KGE models (TransE, ComplEx, DistMult, RotatE).
- `kge_triples_filtered.tsv`: The filtered RDF triple file (subject, predicate, object) used for training.
- `report.docx`: Final project report with methodology, analysis, and answers to tasks.
- `requirements.txt`: Python dependencies required to run the scripts.
- `README.md`: This file.

## 💻 Usage

```bash
pip install -r requirements.txt
python PyKEEN.py
python PyKEEN_Exploitation.py
python PyKEEN_Experiments.py
```

## 📌 Notes

- The RDF file was preprocessed to ensure compatibility with PyKEEN (no literal objects).
- Ensure that you are using Python 3.8+ and a compatible environment (Anaconda recommended).
