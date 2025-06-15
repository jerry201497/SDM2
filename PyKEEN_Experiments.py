from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory

# Load the triples
tf = TriplesFactory.from_path("kge_triples_filtered.tsv")
models = ['TransE', 'ComplEx', 'DistMult', 'RotatE']
results_summary = []

for model_name in models:
    print(f"🔍 Training model: {model_name}")
    result = pipeline(
        model=model_name,
        training=tf,       # ✅ correctly passed
        testing=tf,        # ✅ required to avoid the ValueError
        training_kwargs={"num_epochs": 5},
        random_seed=42,
        device='cpu'
    )
    mrr = result.get_metric("both.realistic.mean_reciprocal_rank")
    results_summary.append((model_name, mrr))

# Save summary to file
with open("kge_model_comparison.txt", "w") as f:
    for model, mrr in results_summary:
        f.write(f"{model}: MRR = {mrr:.4f}\n")
print("✅ Saved model comparison to kge_model_comparison.txt")
