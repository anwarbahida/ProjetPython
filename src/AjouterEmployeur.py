from tkinter import messagebox
from tkinter import *

class AjouterEmployer:
    def __init__(self,frm):
        self.frm=frm
        
        btn = Button(self.frm,text="Ajouter un Employeur",command=self.test)
        btn.pack() 
        
    def test(self):
        messagebox.showinfo("","Ajouter un Employeur")
        
        
        
        
    