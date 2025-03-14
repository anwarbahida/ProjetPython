from datetime import datetime
import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
from db_connection import get_connection
from tkcalendar import DateEntry

from pygame import mixer
class ListePresence:

    def __init__(self,frm,frm1):

        self.frm=frm      
        self.frm.configure(bg="#e0e0e0")
        
        self.frm1=frm1
        
        mixer.init()
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  

        
        titre=Label(self.frm1,text="Liste des Présents",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30,width=300)
        
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
 
        btnRechercher = Button(self.frm, bd=3, relief=GROOVE, text="Rechercher",font=("Arial", 15), background="green", fg="white",command=lambda: self.effectuerRecherche(self.var_critere.get(), txtRechercher.get(), self.date.get_date()) )
        btnRechercher.place(x=850, y=30, width=200, height=33)
        
        self.hoverGreen(btnRechercher)

        Label(self.frm, text="Date : ", bg="#e0e0e0", font=("Arial", 15)).place(x=60, y=90)
        self.date = DateEntry(self.frm, font=("Arial", 12), background="darkblue", foreground="white", borderwidth=2, year=2024)
        self.date.place(x=130, y=90, width=200)
        
        
        btn_afficher = Button(self.frm, text="Afficher les Employés", font=("Arial", 15), bd=4, relief="groove", background="green", fg="white", command=lambda: self.afficher_employés(self.date.get_date()))
        btn_afficher.place(x=60, y=130)
        self.hoverGreen(btn_afficher)
        

        self.tree = ttk.Treeview(self.frm, columns=("ID", "Nom", "Prénom",  "CIN", "Date d'embauche", "Poste", "Genre", "Date et heure", "état"), show="headings")
        
        # Entêtes des colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prénom", text="Prénom")
        self.tree.heading("CIN", text="CIN")
        self.tree.heading("Date d'embauche", text="Date d'embauche")
        self.tree.heading("Poste", text="Poste")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Date et heure", text="Date et heure")
        self.tree.heading("état", text="état")
        
        # Définir la largeur de chaque colonne à 90px
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Nom", width=100, anchor="center")
        self.tree.column("Prénom", width=100, anchor="center")
        self.tree.column("CIN", width=90, anchor="center")
        self.tree.column("Date d'embauche", width=130, anchor="center")
        self.tree.column("Poste", width=100, anchor="center")
        self.tree.column("Genre", width=100, anchor="center")
        self.tree.column("Date et heure", width=150, anchor="center")
        self.tree.column("état", width=150, anchor="center")


        self.tree.pack(fill=BOTH, expand=True)

        # Pack du Treeview
        self.tree.place(x=50,y=220)
    def on_enterGreen(self,event):
        event.widget.config(background="#3CB371", fg="black") 


    def on_leaveGreen(self,event):
        event.widget.config(background="green", fg="white")  
        
    def hoverGreen(self,btn):
        
        btn.bind("<Enter>", self.on_enterGreen)
        btn.bind("<Leave>", self.on_leaveGreen)

    def afficher_employés(self, date):
        
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        mixer.music.play()

        connection = get_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Exécuter la requête SQL pour récupérer les employés présents
                query = """
                    SELECT Employes.id, Employes.nom, Employes.prenom, Employes.cin,
                    Employes.date_embauche, Employes.post, Employes.genre,
                    presence.date_time, presence.entre_sortie
                    FROM Employes
                    INNER JOIN presence ON Employes.id = presence.id_employe
                    WHERE DATE( presence.date_time) = %s
                """
                cursor.execute(query, (date,))
                rows = cursor.fetchall()

                # Effacer les anciens éléments du Treeview
                for row in self.tree.get_children():
                    self.tree.delete(row)

                # Ajouter les données récupérées dans le Treeview
                for row in rows:
                    self.tree.insert("", "end", values=row)

            except mysql.connector.Error as err:
                messagebox.showerror("Erreur", f"Erreur lors de la récupération des données : {err}")
            finally:
                cursor.close()
                connection.close()

    def effectuerRecherche(self, critere, valeur, date):
        
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        mixer.music.play()
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
                    query = """
                    SELECT Employes.id, Employes.nom, Employes.prenom, Employes.cin,
                           Employes.date_embauche, Employes.post, Employes.genre,
                           presence.date_time, presence.entre_sortie
                    FROM Employes
                    INNER JOIN presence ON Employes.id = presence.id_employe
                    WHERE Employes.nom LIKE %s
                    AND DATE(presence.date_time) = %s
                    ORDER BY presence.date_time
                    """
                elif critere == "Poste":
                    query = """
                    SELECT Employes.id, Employes.nom, Employes.prenom, Employes.cin,
                           Employes.date_embauche, Employes.post, Employes.genre,
                           presence.date_time, presence.entre_sortie
                    FROM Employes
                    INNER JOIN presence ON Employes.id = presence.id_employe
                    WHERE Employes.post LIKE %s
                    AND DATE(presence.date_time) = %s
                    ORDER BY presence.date_time
                    """
                else:
                    messagebox.showerror("Erreur", "Critère de recherche invalide.")
                    return

                # Exécuter la requête avec un paramètre LIKE
                cursor.execute(query, (f"%{valeur}%", date))
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
