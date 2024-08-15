import numpy as np
import cv2 as cv
#module pour la 
from keras_facenet import FaceNet
from mtcnn import MTCNN
import os


def extract_face(image, detector, target_size):
    
    # Choisissez un nom de fichier unique pour votre image temporaire
    nom_fichier_temporaire = 'mon_image_temporaire.jpg'
    # Enregistrez l'image temporaire sur le disque
    with open(nom_fichier_temporaire, 'wb') as f:
        f.write(image.read())

    # Lire l'image à partir du fichier temporaire
    img_array = cv.imread(nom_fichier_temporaire)

    # Supprimez le fichier temporaire du disque
    os.remove(nom_fichier_temporaire)

    if img_array is None:
        # Gérer le cas où la lecture de l'image a échoué
        print("Impossible de lire l'image.")
        return None

    # Convertir l'image en RGB
    img = cv.cvtColor(img_array, cv.COLOR_BGR2RGB)

    x, y, w, h = detector.detect_faces(img)[0]['box']
    x, y = abs(x), abs(y)
    face = img_array[y:y+h, x:x+w]
    face_arr = cv.resize(face, target_size)
    print("ALL IS SO GOOOOOOD")
    return face_arr




def calculate_embedding(image):
    # Fonction pour calculer l'embedding de l'image

    embedder = FaceNet()
    
    face_img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    face_img = face_img.astype('float32')
    face_img = np.expand_dims(face_img, axis=0)
    embedding = embedder.embeddings(face_img)[0]

    return embedding

    
from sklearn.metrics.pairwise import cosine_similarity
    




def compare_images_with_label(embeddings,labels,image, label):
    
    # Charger l'image de test et calculer son embedding
    test_embedding = calculate_embedding(image)

    # Récupérer les embeddings correspondant à l'étiquette donnée
    label_embeddings = embeddings[labels == label]

    # Calculer la similarité entre l'embedding de l'image de test et les embeddings correspondants à l'étiquette donnée
    similarities = cosine_similarity([test_embedding], label_embeddings)[0]
    print(similarities)

    # Définir un seuil de similarité
    return similarities.max()



def extract_nv_face(image,detector,target_size):

    img_array = cv.imread(image)
    img = cv.cvtColor(img_array, cv.COLOR_BGR2RGB)

    x, y, w, h = detector.detect_faces(img)[0]['box']
    x, y = abs(x), abs(y)
    face = img_array[y:y+h, x:x+w]
    face_arr = cv.resize(face, target_size)
    print("ALL IS SO GOOOOOOD")
    return face_arr


