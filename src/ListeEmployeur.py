from tkinter import messagebox
from tkinter import *

class ListeEmployeur:
    def __init__(self,frm):
        self.frm=frm
        
        btn=Button(frm,text='list Employeur' ,command=self.message)
        btn.pack()
        
    def message(self):    
        messagebox.showinfo("","Liste des Employeur")