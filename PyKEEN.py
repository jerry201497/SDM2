
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory
from pykeen.models import TransE
import torch

#Load triples correctly using TriplesFactory
tf = TriplesFactory.from_path('kge_triples.tsv')

#Use the TriplesFactory in the pipeline
result = pipeline(
    model='TransE',
    model_kwargs=dict(embedding_dim=50),
    training=tf,
    training_kwargs=dict(num_epochs=100),
    random_seed=42,
    device='cpu'
)

#Access trained embeddings
model = result.model
entity_to_id = tf.entity_to_id
relation_to_id = tf.relation_to_id
entity_embeddings = model.entity_representations[0]().detach().cpu()
relation_embeddings = model.relation_representations[0]().detach().cpu()

#Output confirmation
with open("kge_results.txt", "w") as f:
    f.write("TransE model trained successfully.\n")
    f.write(f"Entities: {len(entity_to_id)}\n")
    f.write(f"Relations: {len(relation_to_id)}\n")
