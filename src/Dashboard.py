from tkinter import Label
import pandas as pd
from PIL import Image, ImageTk
from db_connection import get_connection
import matplotlib.pyplot as plt
from db_connection import get_connection
from tkinter import messagebox
import mysql.connector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Dashboard:
    
    def __init__(self, frm ,frm1):
        self.frm = frm
        self.frm1 = frm1
        
        titre=Label(self.frm1,text="Tableau de bord",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)
        # Afficher l'image
        self.display_image()
        # Afficher le nombre d'employeurs
        self.display_employeur_count()
        self.courb()
        

    def display_image(self):
        """Affiche l'image Employeur.png dans la fenêtre"""
        image = Image.open(".\\images\\Employeur.png")  # Charger l'image
        image = image.resize((100, 100))  # Redimensionner l'image
        photo = ImageTk.PhotoImage(image)  # Convertir l'image en un format compatible avec Tkinter

        # Affichage de l'image dans un label
        self.image_label = Label(self.frm, image=photo)
        self.image_label.image = photo  # Garder une référence de l'image
        self.image_label.place(x=480,y=50,width=100,height=100)

    def display_employeur_count(self):
        
        """Récupère le nombre d'employeurs depuis la base de données et l'affiche"""
        employeur_count = self.get_employeur_count()  # Appel à la fonction pour obtenir le nombre d'employeurs
        count_label = Label(self.frm, text="Employés", font=("consolas", 15))
        count_label.place(x=480,y=10)
        count_label = Label(self.frm, text=f" {employeur_count}", font=("Arial", 14))
        count_label.place(x=510,y=160)

    def get_employeur_count(self):
        
        """Récupère le nombre d'employés depuis la base de données"""
        conn = get_connection()  
        if conn is not None:
            cursor = conn.cursor()

            
            cursor.execute("SELECT COUNT(*) FROM Employes")  
            count = cursor.fetchone()[0]

            cursor.close()
            conn.close() 

            return count
        else:
            return 0  # Si la connexion échoue, on retourne 0 employeurs
        

    def courb(self):
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                query = """
                SELECT DATE(date_time) as date, COUNT(id_employe) as count
                FROM presence
                WHERE date_time BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()
                GROUP BY DATE(date_time)
                ORDER BY DATE(date_time);
                """
                cursor.execute(query)
                rows = cursor.fetchall()

                # Convertir les résultats en DataFrame
                attendance_data = pd.DataFrame(rows, columns=["date", "count"])

                # Tracer le graphique
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(attendance_data["date"], attendance_data["count"], color='skyblue')

                ax.set_xlabel("Date", fontsize=12)
                ax.set_ylabel("Nombre d'employés présents", fontsize=12)
                ax.set_title("Présence des employés sur les 30 derniers jours", fontsize=14)
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Intégrer le graphique dans Tkinter
                canvas = FigureCanvasTkAgg(fig, master=self.frm)
                canvas.draw()
                canvas.get_tk_widget().pack()

            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur lors de la récupération des données: {err}")
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showerror("Erreur", "Connexion à la base de données échouée.")