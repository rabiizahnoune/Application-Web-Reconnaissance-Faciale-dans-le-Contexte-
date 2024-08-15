import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from mtcnn import MTCNN
from reconnaissance.calcule_embading import extract_nv_face
from keras_facenet import FaceNet

def load_faces(dir):
    X = []
    Y = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for sub_dir in os.scandir(dir):
            label = sub_dir.name
            for entry in os.scandir(sub_dir):
                if entry.is_file():
                    futures.append(executor.submit(process_face, entry.path, label))

        for future in tqdm(futures, desc='Loading faces'):
            face, label = future.result()
            if face is not None:
                X.append(face)
                Y.append(label)

    return np.array(X), np.array(Y)

def process_face(image_path, label):
    try:
        face = extract_nv_face(image_path, MTCNN(), (160,160))
        return face, label
    except Exception as e:
        return None, None   

def calculate_embeddings_with_labels(embeddings, labels):
    embedder = FaceNet()
    new_embeddings = embedder.embeddings(embeddings)
    return new_embeddings, labels

def save_embeddings_and_labels(embeddings, labels, filename):
    np.save(filename, {'embeddings': embeddings, 'labels': labels})

# def load_faces( dir):
#       X = []
#       Y = []
#       for sub_dir in tqdm(os.listdir(dir)):
#         label = sub_dir  # Utiliser le nom du sous-répertoire comme label
#         path = os.path.join(dir, sub_dir)
#         for im_name in os.listdir(path):
#             try:
#                 image_path = os.path.join(path, im_name)
#                 single_face = extract_nv_face(image_path,MTCNN(),(160,160))
#                 X.append(single_face)
#                 Y.append(label)
#             except Exception as e:
#                 pass 
#       return np.array(X), np.array(Y)




# def calculate_embeddings_with_labels(embeddings, labels):
#     # Initialiser l'embedder FaceNet
#     embedder = FaceNet()

#     new_embeddings = []

#     for face in embeddings:

#         # Calculer l'embedding
#         embedding = calculate_embedding(face)
#         new_embeddings.append(embedding)
