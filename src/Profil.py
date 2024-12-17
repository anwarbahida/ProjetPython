from tkinter import messagebox
from tkinter import *
from db_connection import get_connection

class Profil:
    def __init__(self, frm,frm1):
        self.frm = frm
        self.frm.config(bg="white")
        self.frm1=frm1
        titre=Label(self.frm1,text="Profil Societe",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)
        
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
        """Affiche les informations actuelles de la société."""
        # Nettoyage de la frame
        for widget in self.frm.winfo_children():
            widget.destroy()

        # Titre
        lbl_titre = Label(self.frm, text="Profil de la Société", font=("Arial", 20, "bold"), bg="white", fg="black")
        lbl_titre.place(x=400, y=50)

        # Informations
        y_offset = 130
        for key, value in self.informations.items():
            lbl_key = Label(self.frm, text=f"{key} :", font=("Arial", 14), bg="white", fg="black", anchor="w")
            lbl_key.place(x=200, y=y_offset)

            lbl_value = Label(self.frm, text=value, font=("Arial", 14, "bold"), bg="white", fg="#0071BC", anchor="w")
            lbl_value.place(x=660, y=y_offset)

            y_offset += 40

        # Bouton Modifier
        btn_modifier = Button(self.frm, text="Modifier les Informations", font=("Arial", 15), bg="#0071BC", fg="white", 
                              command=self.modifier_profil)
        btn_modifier.place(x=400, y=y_offset + 20, width=240, height=40)
        self.hoverBlue(btn_modifier)

    def modifier_profil(self):
        """Affiche un formulaire pour modifier les informations de la société."""
        # Nettoyage de la frame
        for widget in self.frm.winfo_children():
            widget.destroy()

        # Titre
        lbl_titre = Label(self.frm, text="Modifier le Profil de la Société", font=("Arial", 20, "bold"), bg="white", fg="black")
        lbl_titre.place(x=340, y=50)

        # Formulaire de modification
        self.entries = {}
        y_offset = 130  # Décalage vertical pour le formulaire de modification
        
        for key, value in self.informations.items():
            # Label pour le nom de l'information (ex. Nom de la société)
            lbl_key = Label(self.frm, text=f"{key} :", font=("Arial", 14), bg="white", fg="black", anchor="w")
            lbl_key.place(x=200, y=y_offset)

            # Champ de saisie pour la valeur (modification)
            entry_value = Entry(self.frm, font=("Arial", 14), bg="#F0F0F0", fg="black")
            entry_value.insert(0, value)
            entry_value.place(x=660, y=y_offset, width=300, height=30)

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
        """Enregistre les nouvelles informations de la société."""
        try:
            for key, entry in self.entries.items():
                self.informations[key] = entry.get()

            # Message de confirmation
            messagebox.showinfo("Succès", "Les informations ont été mises à jour avec succès.")
            self.afficher_profil()
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
