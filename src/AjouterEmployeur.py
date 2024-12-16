from tkinter import messagebox, filedialog
from tkinter import *
import tkinter
from tkcalendar import DateEntry
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

from db_connection import get_connection  # Pour afficher des images dans tkinter


class AjouterEmployer:
    def __init__(self, frm):
        self.frm = frm
        self.selected_image = None  # Pour conserver l'image sélectionnée

        # Nom
        Label(self.frm, text="Nom: ").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.nom = Entry(self.frm)
        self.nom.grid(row=0, column=1, padx=10, pady=5)

        # Prénom
        Label(self.frm, text="Prénom: ").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.prenom = Entry(self.frm)
        self.prenom.grid(row=1, column=1, padx=10, pady=5)

        # Date de naissance
        Label(self.frm, text="Date de Naissance:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.date_naiss = DateEntry(self.frm, width=12, background="darkblue", foreground="white", borderwidth=2, year=2000)
        self.date_naiss.grid(row=2, column=1, padx=10, pady=5)

        # CIN
        Label(self.frm, text="CIN: ").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.cin = Entry(self.frm)
        self.cin.grid(row=3, column=1, padx=10, pady=5)

        # Genre
        self.var = IntVar(value=1)  # Valeur par défaut
        Label(self.frm, text="Genre: ").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        homme = Radiobutton(self.frm, text="Homme", variable=self.var, value=1)
        homme.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        femme = Radiobutton(self.frm, text="Femme", variable=self.var, value=0)
        femme.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Poste
        Label(self.frm, text="Poste: ").grid(row=6, column=0, sticky="e", padx=10, pady=5)
        posts = ["Développeur", "Chef de projet", "Responsable marketing", "Technicien", "HR Manager"]
        self.combobox = Combobox(self.frm, values=posts, state="readonly")
        self.combobox.set("Choisissez un poste")
        self.combobox.grid(row=6, column=1, padx=10, pady=5)

        # Importer une image
        Label(self.frm, text="Importer une image: ").grid(row=7, column=0, sticky="e", padx=10, pady=5)

        # Fonction pour importer l'image
        def import_image():
            file_path = filedialog.askopenfilename(
                title="Choisir une image",
                filetypes=[("Fichiers image", "*.jpg *.jpeg *.png *.bmp *.gif")]
            )
            if file_path:
                self.display_image(file_path)
                self.image_path = file_path  

        Button(self.frm, text="Parcourir", command=import_image).grid(row=7, column=1, sticky="w", padx=10, pady=5)

        # Canevas pour aperçu d'image
        self.canvas = Canvas(self.frm, width=200, height=200, bg="lightgray")
        self.canvas.grid(row=8, column=1, padx=10, pady=5)

        # Bouton Ajouter
        yes_no = Button(self.frm, text="Ajouter", command=self.stoker_en_bd)
        yes_no.grid(row=9, column=1, sticky="e", padx=10, pady=5)

    # Fonction pour afficher l'image sélectionnée
    def display_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((200, 200))
            self.selected_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(100, 100, image=self.selected_image)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'image : {e}")


        
     # Fonction pour stocker les données en base de données
    def stoker_en_bd(self):
        connection = get_connection()
        if connection:
            try:
                # Récupération des données saisies
                genre = 'Homme' if self.var.get() == 1 else 'Femme'
                post = self.combobox.get()
                photo_blob = image_to_blob(self.image_path)  # Convertir l'image en binaire

                # Requête SQL
                cursor = connection.cursor()
                insert_query = """INSERT INTO Employes (nom, prenom, date_naissance, photo, cin, post, id_admin, genre) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                values = (self.nom.get(), self.prenom.get(), self.date_naiss.get_date(), photo_blob, self.cin.get(), post, 1, genre)

                # Exécution de la requête
                cursor.execute(insert_query, values)
                connection.commit()
                messagebox.showinfo("Succès", "Employé ajouté avec succès!")
                
                self.nom.delete(0, tkinter.END)
                self.prenom.delete(0, tkinter.END)
                self.cin.delete(0, tkinter.END)
                self.combobox.set("Choisissez un poste")
                self.canvas.delete("all") 


            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'employé: {e}")
            finally:
                cursor.close()
                connection.close()



def image_to_blob(file_path):
    with open(file_path, 'rb') as file:
        return file.read()