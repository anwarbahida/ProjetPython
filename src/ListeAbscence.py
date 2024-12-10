from tkinter import messagebox
from tkinter import *

class ListeAbscence:
    def __init__(self,frm):
        self.frm=frm
        
        btn = Button(self.frm,text="Liste des Abscences",command=self.test)
        btn.pack() 
        
    def test(self):
        messagebox.showinfo("","c'est le Liste des Abscences")