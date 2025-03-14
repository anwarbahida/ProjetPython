from tkinter import messagebox
from tkinter import *
from db_connection import get_connection
from pygame import mixer

class Profil:
    def __init__(self, frm,frm1):
        self.frm = frm
        self.frm.config(bg="#e0e0e0")
        self.frm1=frm1
        
        mixer.init()
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        
        titre=Label(self.frm1,text="Profil Societe",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30,width=300)
        
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT societe, id_fiscal, register_commerce, email FROM admines"
        cursor.execute(query,)
        rows = cursor.fetchall()
        for row in rows:
            societe, id_fiscal, register_commerce,email=row
            self.informations = {
                "Nom de la société": f"{societe}",
                "N° Fiscal": f"{id_fiscal}",
                "Registre de commerce": f"{register_commerce}",
                "Email": f"{email}",
            }
            
            self.afficher_profil()

    def afficher_profil(self):
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        mixer.music.play()
        """Affiche les informations actuelles de la société."""
        # Nettoyage de la frame
        for widget in self.frm.winfo_children():
            widget.destroy()

        # Titre
        lbl_titre = Label(self.frm, text="Profil de la Société", font=("Arial", 20, "bold"), bg="#e0e0e0", fg="black")
        lbl_titre.place(x=400, y=50)

        # Informations
        y_offset = 130
        for key, value in self.informations.items():
            lbl_key = Label(self.frm, text=f"{key} :", font=("Arial", 14), bg="#e0e0e0", fg="black", anchor="w")
            lbl_key.place(x=200, y=y_offset)

            lbl_value = Label(self.frm, text=value, font=("Arial", 14, "bold"), bg="#e0e0e0", fg="#0071BC", anchor="w")
            lbl_value.place(x=600, y=y_offset)

            y_offset += 40

        # Bouton Modifier
        btn_modifier = Button(self.frm, text="Modifier les Informations", font=("Arial", 15), bg="#0071BC", fg="white", 
                              command=self.modifier_profil)
        btn_modifier.place(x=400, y=y_offset + 20, width=240, height=40)
        self.hoverBlue(btn_modifier)

    def modifier_profil(self):
        """Affiche un formulaire pour modifier les informations de la société."""
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        mixer.music.play()
        # Nettoyage de la frame
        for widget in self.frm.winfo_children():
            widget.destroy()

        # Titre
        lbl_titre = Label(self.frm, text="Modifier le Profil de la Société", font=("Arial", 20, "bold"), bg="#e0e0e0", fg="black")
        lbl_titre.place(x=340, y=50)

        # Formulaire de modification
        self.entries = {}
        y_offset = 130  # Décalage vertical pour le formulaire de modification
        
        for key, value in self.informations.items():
            # Label pour le nom de l'information (ex. Nom de la société)
            lbl_key = Label(self.frm, text=f"{key} :", font=("Arial", 14), bg="#e0e0e0", fg="black", anchor="w")
            lbl_key.place(x=200, y=y_offset)

            # Champ de saisie pour la valeur (modification)
            entry_value = Entry(self.frm, font=("Arial", 14), bg="#F0F0F0", fg="black")
            entry_value.insert(0, value)
            entry_value.place(x=600, y=y_offset, width=300, height=30)

            # Stocker chaque champ dans un dictionnaire pour l'accès ultérieur
            self.entries[key] = entry_value

            # Incrémentation de l'offset pour le prochain champ
            y_offset += 40

        # Boutons d'action
        btn_save = Button(self.frm, text="Sauvegarder", font=("Arial", 15), bg="green", fg="white", 
                        command=self.sauvegarder_informations)
        btn_save.place(x=300, y=y_offset + 20, width=200, height=40)
        
        self.hoverGreen(btn_save)

        btn_annuler = Button(self.frm, text="Annuler", font=("Arial", 15), bg="red", fg="white", 
                            command=self.afficher_profil)
        btn_annuler.place(x=540, y=y_offset + 20, width=200, height=40)
        self.hoverRed(btn_annuler)


    def sauvegarder_informations(self):
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        mixer.music.play()
        """Enregistre les nouvelles informations de la société."""
        try:
            # Connexion à la base de données
            connection = get_connection()  # Vous devez définir cette fonction pour récupérer la connexion à votre base de données
            cursor = connection.cursor()

            # Préparer la requête SQL pour mettre à jour les informations de la société
            query = """
                UPDATE admines 
                SET societe = %s, id_fiscal = %s, register_commerce = %s, email = %s 
            """
            
            # Récupérer les nouvelles informations depuis les champs
            new_societe = self.entries["Nom de la société"].get()
            new_id_fiscal = self.entries["N° Fiscal"].get()
            new_register_commerce = self.entries["Registre de commerce"].get()
            new_email = self.entries["Email"].get()

            # Exécuter la requête SQL avec les nouvelles valeurs
            cursor.execute(query, (new_societe, new_id_fiscal, new_register_commerce, new_email))

            # Commit des changements
            connection.commit()

            # Mise à jour des informations locales dans l'objet
            self.informations["Nom de la société"] = new_societe
            self.informations["N° Fiscal"] = new_id_fiscal
            self.informations["Registre de commerce"] = new_register_commerce
            self.informations["Email"] = new_email

            # Message de confirmation
            messagebox.showinfo("Succès", "Les informations ont été mises à jour avec succès.")
            
            # Revenir à l'affichage du profil
            self.afficher_profil()
            
            # Fermer la connexion
            cursor.close()
            connection.close()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

            
    def on_enterGreen(self,event):
        event.widget.config(background="#3CB371", fg="black") 


    def on_leaveGreen(self,event):
        event.widget.config(background="green", fg="white")  
        
    def hoverGreen(self,btn):
        
        btn.bind("<Enter>", self.on_enterGreen)
        btn.bind("<Leave>", self.on_leaveGreen)
        
    def on_enterBlue(self,event):
        event.widget.config(background="#27D4FC", fg="black") 


    def on_leaveBlue(self,event):
        event.widget.config(background="#0A82A0", fg="white")  
        
    def hoverBlue(self,btn):
        
        btn.bind("<Enter>", self.on_enterBlue)
        btn.bind("<Leave>", self.on_leaveBlue)
        
        
    def on_enterRed(self,event):
        event.widget.config(background="#DB6F10", fg="black") 


    def on_leaveRed(self,event):
        event.widget.config(background="red", fg="white")  
        
    def hoverRed(self,btn):
        
        btn.bind("<Enter>", self.on_enterRed)
        btn.bind("<Leave>", self.on_leaveRed)
