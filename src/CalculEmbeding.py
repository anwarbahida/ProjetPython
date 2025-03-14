import os
import cv2
import numpy as np
import dlib
import mysql.connector
from PIL import Image
from db_connection import get_connection 

# Initialisation des modèles Dlib
face_rec_model = dlib.face_recognition_model_v1(
    'C:\\Users\\Hp\\ProjetPython\\src\\dlib_face_recognition_resnet_model_v1.dat'
)
shape_predictor = dlib.shape_predictor(
    'C:\\Users\\Hp\\ProjetPython\\src\\shape_predictor_68_face_landmarks.dat'
)
face_detector = dlib.get_frontal_face_detector()

def convert_binary_to_image(binary_data):
    """
    Convertit des données binaires en une image utilisable par OpenCV.
    """
    # Convertir les données binaires en tableau NumPy
    nparr = np.frombuffer(binary_data, np.uint8)
    # Décoder l'image à partir du tableau NumPy
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def calculate_face_embedding_from_binary(binary_data):
    """
    Calcule l'embedding facial à partir d'une image stockée en binaire.
    """
    # Convertir les données binaires en image
    image = convert_binary_to_image(binary_data)
    if image is None:
        print("Erreur lors du décodage de l'image binaire.")
        return None

    # Convertir l'image en RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Détecter le visage
    faces = face_detector(rgb_image)
    if len(faces) == 0:
        print("Aucun visage détecté dans l'image binaire.")
        return None

    # Calculer l'embedding pour le premier visage détecté
    landmarks = shape_predictor(rgb_image, faces[0])
    embedding = np.array(face_rec_model.compute_face_descriptor(rgb_image, landmarks))
    return embedding

def store_embeddings_in_db(employee_id, embedding):
    """
    Stocke l'embedding facial dans la base de données pour un employé donné.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Sauvegarder l'embedding dans la base de données
    sql = "UPDATE employes SET embedding = %s WHERE id = %s"
    cursor.execute(sql, (embedding.tobytes(), employee_id))
    conn.commit()

    cursor.close()
    conn.close()

def process_employees():
    """
    Récupère les employés avec des photos non traitées, calcule leurs embeddings et les stocke dans la base de données.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, photo FROM employes WHERE embedding IS NULL")

    for employee_id, binary_photo in cursor.fetchall():
        print(f"Traitement de l'employé {employee_id}")
        
        # Calculer l'embedding à partir des données binaires
        embedding = calculate_face_embedding_from_binary(binary_photo)
        if embedding is not None:
            store_embeddings_in_db(employee_id, embedding)

    cursor.close()
    conn.close()

# Lancer le traitement
if __name__ == "__main__":
    process_employees()
