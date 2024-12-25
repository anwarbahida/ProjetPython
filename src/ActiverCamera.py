import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from FaceDetection import load_embeddings_from_db,calculate_face_embedding,save_detection_to_db,recognize_face
from datetime import date, datetime,timedelta
from db_connection import get_connection 
import mediapipe as mp
import numpy as np
import dlib

class ActiverCamera:
    def __init__(self, frm,frm1):
        
        self.frm = frm
        self.frm1 = frm1
        self.statue=False
        
        titre=Label(self.frm1,text="Activer Camera",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)

        # Initialisation de la caméra de l'ordinateur (ID de la caméra 0 pour la caméra par défaut)
        self.vid = cv2.VideoCapture(0)

        if not self.vid.isOpened():
            messagebox.showerror("Erreur", "Impossible d'accéder à la caméra de l'ordinateur")

        # Zone de la vidéo (canvas) pour afficher l'image de la caméra
        self.canvas = Canvas(self.frm, width=1054, height=528)
        self.canvas.configure(bg="black")
        self.canvas.place(width=1059,height=528)

        # Bouton pour activer la caméra
        self.btn = Button(self.frm, text="Lancer Caméra",bd=3, relief=GROOVE, font=("Times New Roman", 16),background="green", fg="white" ,command=self.activer_camera)
        self.btn.place(x=450,y=3,height=33)
        
        self.hover(self.btn)
        

        self.is_recording = False
        self.writer = None

    def activer_camera(self):

        # Initialisation de Mediapipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils

        # Charger les embeddings précalculés des employés
        # Format: {"Nom Employé": embedding}
        def load_embeddings_from_db():
            # Connexion à la base de données
            connection = get_connection()
    
            cursor = connection.cursor()

            # Charger les embeddings des employés depuis la base de données
            cursor.execute("SELECT id, nom, embedding FROM employes WHERE embedding IS NOT NULL")

            employee_embeddings = {}
            employee_ids = {}

            for employee_id, employee_name, embedding in cursor.fetchall():
                # Convertir l'embedding binaire en un tableau numpy
                embedding_array = np.frombuffer(embedding, dtype=np.float64)
                # Ajouter l'embedding dans le dictionnaire avec le nom de l'employé
                employee_embeddings[employee_name] = embedding_array

                employee_ids[employee_name] = employee_id

            cursor.close()
            connection.close()

            return employee_embeddings, employee_ids

        # Charger les embeddings et les ids depuis la base de données
        employee_embeddings, employee_ids = load_embeddings_from_db()

        face_rec_model = dlib.face_recognition_model_v1('C:\\Users\\ADDICHANE\\OneDrive\\Documents\\Projet_Python\\ProjetPython\\src\\dlib_face_recognition_resnet_model_v1.dat')
        shape_predictor = dlib.shape_predictor('C:\\Users\\ADDICHANE\\OneDrive\\Documents\\Projet_Python\\ProjetPython\\src\\shape_predictor_68_face_landmarks.dat')



        # Dernières détections (en mémoire)
        last_detections = {}  # Format: {employee_id: datetime}


        def calculate_face_embedding(image, bbox):
            """
            Calculer un embedding facial à partir de l'image et de la bounding box en utilisant Dlib.
            """
            x, y, w, h = bbox
    
            # Extraire la région du visage à partir de la bounding box
            face = image[y:y+h, x:x+w]

            # Convertir le visage en RGB si nécessaire (Dlib utilise RGB)
            if len(face.shape) == 3 and face.shape[2] == 3:
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    
            # Initialiser le détecteur de visages Dlib
            detector = dlib.get_frontal_face_detector()

            # Détecter le visage
            faces = detector(face, 1)
            if len(faces) == 0:
                return None

            # Utiliser le premier visage détecté
            face_rect = faces[0]
    
            # Extraire les points de repère (landmarks)
            landmarks = shape_predictor(face, face_rect)

            # Calculer l'embedding
            embedding = np.array(face_rec_model.compute_face_descriptor(face, landmarks))

            return embedding



        def save_detection_to_db(employee_id, detection_time):
            """
            Insère une détection dans la base de données et détermine automatiquement "entrée" ou "sortie".
            """
            connection = get_connection()
            cursor = connection.cursor()

            try:
                # Convertir `detection_time` en objet datetime si ce n'est pas déjà le cas
                if isinstance(detection_time, str):
                    detection_time = datetime.strptime(detection_time, "%Y-%m-%d %H:%M:%S")
                    # Récupérer la dernière détection de cet employé pour la journée en cours
                cursor.execute(
                 "SELECT id, entre_sortie FROM presence WHERE id_employe = %s AND DATE(date_time) = %s ORDER BY date_time DESC LIMIT 1",
                (employee_id, detection_time.date())
                )
                last_detection = cursor.fetchone()

                # Déterminer si c'est une "entrée" ou une "sortie"
                entre_sortie = 'entrée' if not last_detection or last_detection[1] == 'sortie' else 'sortie'
        

                # Insérer la nouvelle détection
                cursor.execute(
                 "INSERT INTO presence (id_employe, date_time, entre_sortie) VALUES (%s, %s, %s)",
                (employee_id, detection_time, entre_sortie)
                 )
                connection.commit()
                print(f"Détection enregistrée : Employé ID {employee_id}, {entre_sortie} à {detection_time}")

            except Exception as e:
                print(f"Erreur lors de l'enregistrement de la détection : {e}")
            finally:
                cursor.close()
                connection.close()


        def recognize_face(embedding):
            name = "Inconnu"
            min_distance = float("inf")
            for employee_name, employee_embedding in employee_embeddings.items():
                distance = np.linalg.norm(employee_embedding - embedding)
                if distance < 0.6 and distance < min_distance:  # Seuil de reconnaissance
                    min_distance = distance
                    name = employee_name
            return name
                # Capture vidéo
        cap = cv2.VideoCapture(0)

        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Erreur de capture vidéo.")
                    break

                # Conversion en RGB pour Mediapipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(rgb_frame)

                name = "Inconnu"  # Nom par défaut
                employee_id = None  # ID par défaut

                if results.detections:
                    for detection in results.detections:
                        # Extraire la bounding box
                        bboxC = detection.location_data.relative_bounding_box
                        ih, iw, _ = frame.shape
                        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                                    int(bboxC.width * iw), int(bboxC.height * ih)
                
                        # Calculer l'embedding du visage détecté
                        embedding = calculate_face_embedding(frame, (x, y, w, h))
                        if embedding is None:
                            continue  # Passer au visage suivant si aucun embedding n'a été généré

                        # Reconnaître le visage
                        name = recognize_face(embedding)

                        # Annoter l'image avec le nom
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                        # Après avoir parcouru toutes les détections, enregistrer la détection (si un nom valide a été détecté)
            
                    if name != "Inconnu":
                        employee_id = employee_ids.get(name, None)
                        if employee_id:
                            current_time = datetime.now()
                            last_time = last_detections.get(employee_id, None)
                        
                            # Enregistrement si la dernière détection dépasse 20 secondes
                            if not last_time or (current_time - last_time > timedelta(seconds=20)):
                                last_detections[employee_id] = current_time
                                save_detection_to_db(employee_id, current_time)

                # Afficher le flux vidéo avec les annotations
                cv2.imshow('Reconnaissance Faciale', frame)

                if cv2.waitKey(10) & 0xFF == 27:  # Quitter avec la touche 'ESC'
                    break

        cap.release()
        cv2.destroyAllWindows()

    def update_video(self):
        ret, frame = self.vid.read()

        if ret:
            # Appliquer le filtre si nécessaire
            if hasattr(self, 'filter') and self.filter:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convertir l'image BGR en RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            

            # Convertir le frame en image utilisable dans Tkinter
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Afficher l'image dans le canvas
            self.canvas.create_image(200, 40, anchor=NW, image=img_tk)

            # Maintenir la référence de l'image
            self.canvas.img_tk = img_tk

            # Mettre à jour le flux vidéo
            self.canvas.after(10, self.update_video)


    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.writer:
            self.writer.release()
            
    def on_enter(self,event):
        event.widget.config(background="#3CB371", fg="black") 


    def on_leave(self,event):
        event.widget.config(background="green", fg="white")  
        
    def hover(self,btn):
        
        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)