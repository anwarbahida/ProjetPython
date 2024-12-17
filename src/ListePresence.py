from tkinter import messagebox
from tkinter import *

class ListePresence:
    def __init__(self,frm,frm1):
        self.frm=frm
        
        self.frm1=frm1
        titre=Label(self.frm1,text="Liste Presence",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)
        
        btn = Button(self.frm,text="Liste des Prescences",command=self.test)
        btn.pack() 
        
    def test(self):
        messagebox.showinfo("","c'est le Liste des Prescences")