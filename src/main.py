
from tkinter import *
import os
from Dashboard import Dashboard
from AjouterEmployeur import AjouterEmployer
from ListeEmployeur import ListeEmployeur
from ListeAbscence import ListeAbscence
from ListePresence import ListePresence
from Profil import Profil
from ActiverCamera import *
from Rapport import Rapport
from pygame import mixer

class main:
    
    #fonction d'interface graphique
    def __init__(self):
        
        
        mixer.init()
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        
        self.interface()
        
    def destroy_frame(self):
        
        for widget in self.frm3.winfo_children() :
            widget.destroy()
        
    def on_enter(self,event):
        event.widget.config(background="#3CB371", fg="black") 


    def on_leave(self,event):
        event.widget.config(background="green", fg="white")  
        
    def hover(self,btn):
        
        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)
    
    def SeDeconnecter(self):
        self.root.destroy()
        
    # Fonction d'interface graphique
    def interface(self):
        self.root = Tk()
        self.root.title("Pointage d'employés")
        self.root.geometry("1350x700+100+60")
        icon_path = os.path.join(os.path.dirname(__file__), "../images/Logo.ico")
        self.root.iconbitmap(icon_path)
        self.root.resizable(False, False)
        self.root.configure(background="#0071BC", bd=3, relief=GROOVE)
        

        lbltitre = Label(self.root, text="Pointage des Employés", bd=3, relief=GROOVE, 
                        font=("Consolas", 25), bg='#F7941D', fg='#FFFAFA')
        lbltitre.place(width=1345, height=70)

        self.frm1 = Frame(self.root,background="green", bd=3, relief=GROOVE)
        self.frm1.place(width=280, height=630, x=0, y=70)

        self.frm2 = Frame(self.root, background="gray", bd=3, relief=GROOVE)
        self.frm2.place(width=1065, height=630, x=280, y=70)

        self.frm3 = Frame(self.frm2, bd=3, relief=GROOVE)
        self.frm3.place(width=1059, height=528, x=0, y=94)
        Dashboard(self.frm3,self.frm2)

        # ________________________________________________________Frame 1_______________________________________________________
        
        
        buttons_info = [
            ("Tableau de Bord", 0),
            ("Liste des Employés", 62),
            ("Ajouter un Employé", 122),
            ("Liste des Absences", 182),
            ("Liste des Présences",242),
            ("Activer Caméra",302),
            ("Rapport Statistique",362),
            ("Profil", 422),
            ("Se Déconnecter", 482),
        ]
        commandes =[
            self.TableauBord,
            self.ListeEmployeur,
            self.AjouterEmployeur,
            self.ListeAbsence,
            self.ListePresence,
            self.ActiverCamera,
            self.RapportStatisique,
            self.Profil,
            self.SeDeconnecter
        ]

        for (text, y), command in zip(buttons_info, commandes):
            btn = Button(self.frm1, text=text, bd=3, relief=GROOVE, font=("Times New Roman", 16),
                        background="green", fg="white", command=command)
            btn.place(x=0, y=y, width=275, height=65)
            
            self.hover(btn)
        
        
        
        # Exécution
        self.root.mainloop()
        
        
    #_________________________________________________________Frame 3__________________________________________________________
        
    #les fonctions dyal les bouton f sidebar
    
    def TableauBord(self):
        self.destroy_frame()
        Dashboard(self.frm3,self.frm2)
        
    def ListeEmployeur(self):
        self.destroy_frame()
        ListeEmployeur(self.frm3,self.frm2)
        
    def AjouterEmployeur(self):
        self.destroy_frame()
        AjouterEmployer(self.frm3,self.frm2)
        
    def ListeAbsence(self):
        self.destroy_frame()
        ListeAbscence(self.frm3,self.frm2)
        
    def ListePresence(self):
        self.destroy_frame()
        ListePresence(self.frm3,self.frm2)
        
    def Profil(self):
        self.destroy_frame()
        Profil(self.frm3,self.frm2)
    
    def ActiverCamera(self):
        self.destroy_frame()
        ActiverCamera(self.frm3,self.frm2)
        
    def RapportStatisique(self):
        self.destroy_frame()
        Rapport (self.frm3,self.frm2)
    