from tkinter import messagebox
from tkinter import *

class Dashbord:
    def __init__(self,frm):
        self.frm=frm
        
        btn = Button(self.frm,text="Dashbord",command=self.test)
        btn.pack() 
           
    def test(self):
        messagebox.showinfo("","c'est le Tableau de Bord")
        