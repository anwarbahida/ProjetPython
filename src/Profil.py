from tkinter import messagebox
from tkinter import *

class Profil:
    def __init__(self,frm):
        self.frm=frm
        
        btn = Button(self.frm,text="Profil",command=self.test)
        btn.pack() 
        
    def test(self):
        messagebox.showinfo("","c'est le Profil")