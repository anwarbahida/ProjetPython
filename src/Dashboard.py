from tkinter import Label
from PIL import Image, ImageTk
from db_connection import get_connection

class Dashboard:
    def __init__(self, frm,frm1):
        self.frm = frm
        self.frm1 = frm1
        
        titre=Label(self.frm1,text="Tableau de Borde",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)
        # Afficher l'image
        self.display_image()

        # Afficher le nombre d'employeurs
        self.display_employeur_count()

    def display_image(self):
        """Affiche l'image Employeur.png dans la fenêtre"""
        image = Image.open("C:\\Users\\ADDICHANE\\OneDrive\\Documents\\Projet_Python\\ProjetPython\\images\\Employeur.png")  # Charger l'image
        image = image.resize((100, 100))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)  # Convertir l'image en un format compatible avec Tkinter

        # Affichage de l'image dans un label
        self.image_label = Label(self.frm, image=photo)
        self.image_label.image = photo  # Garder une référence de l'image
        self.image_label.place(x=480,y=50,width=100,height=100)

    def display_employeur_count(self):
        
        """Récupère le nombre d'employeurs depuis la base de données et l'affiche"""
        employeur_count = self.get_employeur_count()  # Appel à la fonction pour obtenir le nombre d'employeurs
        count_label = Label(self.frm, text="Employes", font=("consolas", 15))
        count_label.place(x=480,y=10)
        count_label = Label(self.frm, text=f" {employeur_count}", font=("Arial", 14))
        count_label.place(x=510,y=160)

    def get_employeur_count(self):
        
        """Récupère le nombre d'employeurs depuis la base de données"""
        conn = get_connection()  # Appel à la fonction get_connection pour obtenir la connexion
        if conn is not None:
            cursor = conn.cursor()

            # Exécution de la requête pour compter les employeurs
            cursor.execute("SELECT COUNT(*) FROM Employes")  # Remplacez 'employeurs' par le nom de votre table
            count = cursor.fetchone()[0]

            cursor.close()
            conn.close()  # Assurez-vous de fermer la connexion après l'utilisation

            return count
        else:
            return 0  # Si la connexion échoue, on retourne 0 employeurs
