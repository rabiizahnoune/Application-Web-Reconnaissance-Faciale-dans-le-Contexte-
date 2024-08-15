import django
django.setup()
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face.settings')


import numpy as np

from reconnaissance.models import EmbeddingModel


def load_embeddings_to_database(file_path):
    # Chargez les embeddings et les étiquettes à partir du fichier .npy
    data = np.load(file_path, allow_pickle=True)
    embeddings = data['embeddings']
    labels = data['labels']
    for embedding, label in zip(embeddings, labels):
        embedding_model = EmbeddingModel(embedding=embedding.tobytes(), label=label)
        embedding_model.save()

file_path = "C:\hello\reconnaissance\fichier de projet\fichier.npy"
load_embeddings_to_database(file_path)


