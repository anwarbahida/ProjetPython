from tkinter import messagebox
from tkinter import *

class ActiverCamera:
    def __init__(self,frm):
        self.frm=frm
        
        btn = Button(self.frm,text="Camera",command=self.test)
        btn.pack() 
           
    def test(self):
        messagebox.showinfo("","c'est la partie d'activation de Camera")