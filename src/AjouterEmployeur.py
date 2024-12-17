from tkinter import messagebox, filedialog
from tkinter import *
import tkinter
import mysql.connector
from io import BytesIO
from tkcalendar import DateEntry
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from db_connection import get_connection  # Pour afficher des images dans tkinter


class AjouterEmployer:
    def __init__(self, frm,frm1):
        self.frm = frm
        self.frm1=frm1
        titre=Label(self.frm1,text="Ajouter Employes",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)
        self.frm.config(bg="#f5f5f5")  # Changer le fond du formulaire pour un léger gris

        # Cadre pour les informations personnelles
        self.frame_personal_info = Frame(self.frm, bg="#e0e0e0", bd=2, relief=SOLID)
        self.frame_personal_info.place(x=10, y=10, width=600, height=220)

        # Nom
        Label(self.frame_personal_info, text="Nom: ", bg="#e0e0e0", font=("Arial", 12)).place(x=10, y=20)
        self.nom = Entry(self.frame_personal_info, font=("Arial", 12))
        self.nom.place(x=150, y=20, width=300)

        # Prénom
        Label(self.frame_personal_info, text="Prénom: ", bg="#e0e0e0", font=("Arial", 12)).place(x=10, y=60)
        self.prenom = Entry(self.frame_personal_info, font=("Arial", 12))
        self.prenom.place(x=150, y=60, width=300)

        # Date de naissance
        Label(self.frame_personal_info, text="Date de Naissance: ", bg="#e0e0e0", font=("Arial", 12)).place(x=10, y=100)
        self.date_naiss = DateEntry(self.frame_personal_info, font=("Arial", 12), background="darkblue", foreground="white", borderwidth=2, year=2000)
        self.date_naiss.place(x=150, y=100, width=300)

        # CIN
        Label(self.frame_personal_info, text="CIN: ", bg="#e0e0e0", font=("Arial", 12)).place(x=10, y=140)
        self.cin = Entry(self.frame_personal_info, font=("Arial", 12))
        self.cin.place(x=150, y=140, width=300)

        # Cadre pour les informations supplémentaires
        self.frame_additional_info = Frame(self.frm, bg="#e0e0e0", bd=2, relief=SOLID)
        self.frame_additional_info.place(x=10, y=250, width=600, height=220)

        # Genre
        self.var = IntVar(value=1)  # Valeur par défaut
        Label(self.frame_additional_info, text="Genre: ", bg="#e0e0e0", font=("Arial", 12)).place(x=10, y=20)
        homme = Radiobutton(self.frame_additional_info, text="Homme", variable=self.var, value=1, font=("Arial", 12), bg="#e0e0e0")
        homme.place(x=150, y=20)
        femme = Radiobutton(self.frame_additional_info, text="Femme", variable=self.var, value=0, font=("Arial", 12), bg="#e0e0e0")
        femme.place(x=300, y=20)

        # Poste
        Label(self.frame_additional_info, text="Poste: ", bg="#e0e0e0", font=("Arial", 12)).place(x=10, y=80)
        posts = ["Développeur", "Chef de projet", "Responsable marketing", "Technicien", "HR Manager"]
        self.combobox = Combobox(self.frame_additional_info, values=posts, state="readonly", font=("Arial", 12))
        self.combobox.set("Choisissez un poste")
        self.combobox.place(x=150, y=80, width=300)

        # Importer une image
        Label(self.frame_additional_info, text="Importer une image: ", bg="#e0e0e0", font=("Arial", 12)).place(x=10, y=140)

        # Fonction pour importer l'image
        def import_image():
            file_path = filedialog.askopenfilename(
                title="Choisir une image",
                filetypes=[("Fichiers image", "*.jpg *.jpeg *.png *.bmp *.gif")]
            )
            if file_path:
                self.display_image(file_path)
                self.image_path = file_path  

        btn=Button(self.frame_additional_info, text="Parcourir", command=import_image, font=("Arial", 12), bg="#4CAF50", fg="white")
        btn.place(x=200, y=140)
        self.hover(btn)

        # Canevas pour aperçu d'image à côté des champs
        self.canvas = Canvas(self.frm, width=300, height=300, bg="lightgray")
        self.canvas.place(x=700, y=100)

        # Bouton Ajouter
        yes_no = Button(self.frm, text="Ajouter",bd=4,relief="groove", command=self.stoker_en_bd, font=("Arial", 16), bg="green", fg="white")
        yes_no.place(x=465, y=475,width=150)
        
        self.hover(yes_no)
        
    def on_enter(self,event):
        event.widget.config(background="#3CB371", fg="black") 


    def on_leave(self,event):
        event.widget.config(background="green", fg="white")  
        
    def hover(self,btn):
        
        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)

    def display_image(self, file_path):
        
        # Logic to display the image in the canvas
        img = Image.open(file_path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)  # Redimensionner l'image
        img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(150, 150, image=img_tk)
        self.canvas.image = img_tk  # Garder une référence à l'image pour éviter qu'elle ne soit collectée par le garbage collector
        

    def image_to_blob(image_path):
        
        try:
            with Image.open(image_path) as img:
                byte_io = BytesIO()
                img.save(byte_io, format="PNG")  # Vous pouvez changer le format si nécessaire
                byte_io.seek(0)
                return byte_io.read()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la conversion de l'image: {e}")
            return None

    def stoker_en_bd(self):
        connection = get_connection()  # Assurez-vous que cette fonction est définie
        if connection:
            try:
                # Récupération des données saisies
                genre = 'Homme' if self.var.get() == 1 else 'Femme'
                post = self.combobox.get()

                # Convertir l'image en binaire
                photo_blob = image_to_blob(self.image_path)
                if photo_blob is None:
                    return  # Si l'image n'a pas pu être convertie, on arrête l'exécution

                # Requête SQL
                cursor = connection.cursor()
                insert_query = """INSERT INTO Employes (nom, prenom, date_naissance, photo, cin, post, id_admin, genre) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
                values = (self.nom.get(), self.prenom.get(), self.date_naiss.get_date(), photo_blob, self.cin.get(), post, 1, genre)

                # Exécution de la requête
                cursor.execute(insert_query, values)
                connection.commit()
                messagebox.showinfo("Succès", "Employé ajouté avec succès!")

                # Réinitialiser les champs après ajout
                self.nom.delete(0, tkinter.END)
                self.prenom.delete(0, tkinter.END)
                self.cin.delete(0, tkinter.END)
                self.combobox.set("Choisissez un poste")
                self.canvas.delete("all") 

            except mysql.connector.Error as e:
                messagebox.showerror("Erreur MySQL", f"Erreur lors de l'ajout de l'employé : {e}")
                print(e)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur inconnue : {e}")
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()



def image_to_blob(file_path):
    with open(file_path, 'rb') as file:
        return file.read()