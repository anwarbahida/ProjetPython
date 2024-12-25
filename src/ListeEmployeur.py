import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
from db_connection import get_connection

# Connexion à la base de données MySQL 

# Classe ListeEmployeur avec gestion avancée
class ListeEmployeur:
    
    def __init__(self, frm,frm1):
        
        self.frm = frm
        self.frm.configure(bg="#e0e0e0")
        
        self.frm1=frm1
        titre=Label(self.frm1,text="Lister Employes",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)
        
        lblRech = Label(self.frm, text="Effectuer une Recherche : ", font=("Arial", 15), fg='black', bg="#e0e0e0")
        lblRech.place(x=60, y=30)

        txtRechercher = Entry(self.frm, bd=3, font=('Arial', 14))
        txtRechercher.place(x=300, y=30, width=200)

        # Radiobuttons pour le critère de recherche
        self.var_critere = StringVar() 

        self.lbl_critere = Label(self.frm, text="Critère :", font=("Arial", 15), fg='black', bg="#e0e0e0")
        self.lbl_critere.place(x=520, y=30)

        self.radio_nom = Radiobutton(self.frm, text="Nom", variable=self.var_critere, value="Nom", font=("Arial", 15), fg='black', bg="#e0e0e0")
        self.radio_nom.place(x=650, y=30)

        self.radio_poste = Radiobutton(self.frm, text="Poste", variable=self.var_critere, value="Poste", font=("Arial", 15), fg='black', bg="#e0e0e0")
        self.radio_poste.place(x=730, y=30)
 
        btnRechercher = Button(self.frm, bd=3, relief=GROOVE, text="Rechercher",font=("Arial", 15), background="green", fg="white",command=lambda: self.effectuerRecherche(self.var_critere.get(), txtRechercher.get()) )
        btnRechercher.place(x=850, y=30, width=200, height=33)
        
        self.hoverGreen(btnRechercher)
        
        
        
        btn_afficher = Button(self.frm, text="Afficher les Employés",font=("Arial", 15),bd=4,relief="groove", background="green", fg="white", command=self.afficher_employeurs)
        btn_afficher.place(x=90,y=120)
        self.hoverGreen(btn_afficher)
        
        btn_supprimer = Button(frm, text="Supprimer l'Employé",font=("Arial", 15),bd=4,relief="groove", background="red", fg="white", command=self.supprimer_employe)
        btn_supprimer.place(x=430,y=120)
        self.hoverRed(btn_supprimer)
        
        btn_modifier = Button(frm, text="Modifier l'Employés",font=("Arial", 15),bd=4,relief="groove", background="#0A82A0", fg="white", command=self.modifier_employe)
        btn_modifier.place(x=750,y=120)
        self.hoverBlue(btn_modifier)
        
        self.tree = ttk.Treeview(self.frm, columns=("ID", "Nom", "Prénom", "Date de naissance", "CIN", "Date d'embauche", "Poste", "Genre"), show="headings")
        
        # Entêtes des colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prénom", text="Prénom")
        self.tree.heading("Date de naissance", text="Date de naissance")
        self.tree.heading("CIN", text="CIN")
        self.tree.heading("Date d'embauche", text="Date d'embauche")
        self.tree.heading("Poste", text="Poste")
        self.tree.heading("Genre", text="Genre")
        
        # Définir la largeur de chaque colonne à 90px
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Nom", width=150, anchor="center")
        self.tree.column("Prénom", width=150, anchor="center")
        self.tree.column("Date de naissance", width=100, anchor="center")
        self.tree.column("CIN", width=90, anchor="center")
        self.tree.column("Date d'embauche", width=130, anchor="center")
        self.tree.column("Poste", width=150, anchor="center")
        self.tree.column("Genre", width=150, anchor="center")

        # Pack du Treeview
        self.tree.place(x=50,y=220)
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

    def afficher_employeurs(self):
        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Exécuter la requête SQL pour récupérer les employés
                cursor.execute("SELECT id, nom, prenom, date_naissance, cin, date_embauche, post, genre FROM Employes")
                rows = cursor.fetchall()

                # Effacer les anciens éléments du Treeview
                for row in self.tree.get_children():
                    self.tree.delete(row)

                # Ajouter les données récupérées dans le Treeview
                for row in rows:
                    self.tree.insert("", "end", values=row)

            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur lors de la récupération des données: {err}")
            finally:
                cursor.close()
                connection.close()

    def supprimer_employe(self):
        selected_item = self.tree.selection()
        if selected_item:
            employe_id = self.tree.item(selected_item, "values")[0]  # Récupérer l'ID de l'employé
            confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer l'employé ID {employe_id}?")
            if confirmation:
                connection = get_connection()
                if connection:
                    cursor = connection.cursor()
                    try:
                        # Requête pour supprimer l'employé
                        cursor.execute("DELETE FROM Employes WHERE id = %s", (employe_id,))
                        connection.commit()
                        self.tree.delete(selected_item)  # Supprimer l'employé du Treeview
                        messagebox.showinfo("Succès", "Employé supprimé avec succès!")
                    except mysql.connector.Error as err:
                        messagebox.showerror("Erreur", f"Erreur lors de la suppression de l'employé: {err}")
                    finally:
                        cursor.close()
                        connection.close()
        else:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un employé à supprimer.")

    def modifier_employe(self):
        selected_item = self.tree.selection()
        if selected_item:
            employe_id = self.tree.item(selected_item, "values")[0]  # Récupérer l'ID de l'employé
            # Ouvrir une nouvelle fenêtre pour modifier les détails de l'employé
            modification_window = Toplevel(self.frm)
            modification_window.title(f"Modifier l'Employé ID {employe_id}")
            modification_window.geometry("1059x500+385+260")
            modification_window.resizable(False, False)
            modification_window.config(bd=3, relief="groove",bg='lightgray')

            # Récupérer les informations actuelles de l'employé
            connection = get_connection()
            if connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("SELECT nom, prenom, date_naissance, cin, date_embauche, post, genre FROM Employes WHERE id = %s", (employe_id,))
                    result = cursor.fetchone()
                    if result:
                        nom, prenom, date_naissance, cin, date_embauche, post, genre = result

                        # Création des champs de saisie avec place() pour une meilleure organisation
                        label_nom = Label(modification_window,font=("Arial", 15), text="Nom:",bg='lightgray')
                        label_nom.place(x=220, y=30)
                        entry_nom = Entry(modification_window,font=("Arial", 13))
                        entry_nom.place(x=600, y=30,height=33, width=220)

                        label_prenom = Label(modification_window,font=("Arial", 15), text="Prénom:",bg='lightgray')
                        label_prenom.place(x=220, y=80)
                        entry_prenom = Entry(modification_window,font=("Arial", 13))
                        entry_prenom.place(x=600, y=80,height=33, width=220)

                        label_date_naissance = Label(modification_window,font=("Arial", 15), text="Date de naissance (YYYY-MM-DD):",bg='lightgray')
                        label_date_naissance.place(x=220, y=130)
                        entry_date_naissance = Entry(modification_window,font=("Arial", 13))
                        entry_date_naissance.place(x=600, y=130,height=33, width=220)

                        label_cin = Label(modification_window,font=("Arial", 15), text="CIN:",bg='lightgray')
                        label_cin.place(x=220, y=180)
                        entry_cin = Entry(modification_window,font=("Arial", 13))
                        entry_cin.place(x=600, y=180,height=33, width=220)

                        label_date_embauche = Label(modification_window,font=("Arial", 15), text="Date d'embauche (YYYY-MM-DD):",bg='lightgray')
                        label_date_embauche.place(x=220, y=230)
                        entry_date_embauche = Entry(modification_window,font=("Arial", 13))
                        entry_date_embauche.place(x=600, y=230,height=33, width=220)

                        label_post = Label(modification_window,font=("Arial", 15), text="Poste:",bg='lightgray')
                        label_post.place(x=220, y=280)
                        entry_post = Entry(modification_window,font=("Arial", 13))
                        entry_post.place(x=600, y=280,height=33, width=220)

                        label_genre = Label(modification_window,font=("Arial", 15), text="Genre:",bg='lightgray')
                        label_genre.place(x=220, y=330)
                        entry_genre = Entry(modification_window,font=("Arial", 13))
                        entry_genre.place(x=600, y=330,height=33, width=220)

                        # Pré-remplir les champs avec les données actuelles
                        entry_nom.insert(0, nom)
                        entry_prenom.insert(0, prenom)
                        entry_date_naissance.insert(0, date_naissance)
                        entry_cin.insert(0, cin)
                        entry_date_embauche.insert(0, date_embauche)
                        entry_post.insert(0, post)
                        entry_genre.insert(0, genre)

                        # Fonction pour sauvegarder les modifications
                        def save_changes():
                            # Récupérer les valeurs mises à jour
                            updated_nom = entry_nom.get()
                            updated_prenom = entry_prenom.get()
                            updated_date_naissance = entry_date_naissance.get()
                            updated_cin = entry_cin.get()
                            updated_date_embauche = entry_date_embauche.get()
                            updated_post = entry_post.get()
                            updated_genre = entry_genre.get()

                            # Rouvrir la connexion et recréer le curseur à chaque modification
                            connection = get_connection()  # S'assurer que vous récupérez une connexion active
                            if connection:
                                cursor = connection.cursor()
                                try:
                                    # Requête pour mettre à jour l'employé
                                    cursor.execute("""
                                        UPDATE Employes SET nom = %s, prenom = %s, date_naissance = %s, cin = %s, date_embauche = %s, post = %s, genre = %s WHERE id = %s
                                    """, (updated_nom, updated_prenom, updated_date_naissance, updated_cin, updated_date_embauche, updated_post, updated_genre, employe_id))
                                    connection.commit()
                                    messagebox.showinfo("Succès", "Employé mis à jour avec succès!")
                                    modification_window.destroy()
                                    self.afficher_employeurs()  # Rafraîchir la liste des employés
                                except mysql.connector.Error as err:
                                    messagebox.showerror("Erreur", f"Erreur lors de la mise à jour des données: {err}")
                                finally:
                                    cursor.close()
                                    connection.close()  # Fermer la connexion après utilisation

                        # Bouton pour sauvegarder les modifications
                        save_button = Button(modification_window, text="Sauvegarder",font=("Arial", 15),bd=4,relief=GROOVE ,background="#0A82A0", fg="white", command=save_changes)
                        save_button.place(x=440, y=400, width=200)
                        
                        self.hoverBlue(save_button)

                except mysql.connector.Error as err:
                    messagebox.showerror("Erreur", f"Erreur lors de la récupération des données: {err}")
                finally:
                    cursor.close()
                    connection.close()
        else:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un employé à modifier.")
            
    def effectuerRecherche(self, critere, valeur):
        
        """ Effectue une recherche selon le critère sélectionné et la valeur saisie. """
        connection = get_connection()
        if not valeur.strip():  # Si le champ de recherche est vide
            messagebox.showwarning("Attention", "Veuillez saisir une valeur pour la recherche.")
            return

        if connection:
            cursor = connection.cursor()
            try:
                # Construire la requête SQL en fonction du critère
                if critere == "Nom":
                    query = "SELECT id, nom, prenom, date_naissance, cin, date_embauche, post, genre FROM Employes WHERE nom LIKE %s"
                elif critere == "Poste":
                    query = "SELECT id, nom, prenom, date_naissance, cin, date_embauche, post, genre FROM Employes WHERE post LIKE %s"
                else:
                    messagebox.showerror("Erreur", "Critère de recherche invalide.")
                    return

                # Exécuter la requête avec un paramètre LIKE
                cursor.execute(query, (f"%{valeur}%",))
                rows = cursor.fetchall()

                # Effacer les anciennes données dans le Treeview
                for row in self.tree.get_children():
                    self.tree.delete(row)

                # Insérer les résultats dans le Treeview
                if rows:
                    for row in rows:
                        self.tree.insert("", "end", values=row)
                else:
                    messagebox.showinfo("Résultat", "Aucun résultat trouvé.")

            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur lors de la recherche : {err}")
            finally:
                cursor.close()
                connection.close()

