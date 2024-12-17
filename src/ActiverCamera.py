import cv2
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

class ActiverCamera:
    def __init__(self, frm,frm1):
        
        self.frm = frm
        self.frm1 = frm1
        self.statue=False
        
        titre=Label(self.frm1,text="Activer Camera",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30)

        # Initialisation de la caméra de l'ordinateur (ID de la caméra 0 pour la caméra par défaut)
        self.vid = cv2.VideoCapture(0)

        if not self.vid.isOpened():
            messagebox.showerror("Erreur", "Impossible d'accéder à la caméra de l'ordinateur")

        # Zone de la vidéo (canvas) pour afficher l'image de la caméra
        self.canvas = Canvas(self.frm, width=1054, height=528)
        self.canvas.configure(bg="black")
        self.canvas.place(width=1059,height=528)

        # Bouton pour activer la caméra
        self.btn = Button(self.frm, text="Lancer Caméra",bd=3, relief=GROOVE, font=("Times New Roman", 16),background="green", fg="white" ,command=self.activer_camera)
        self.btn.place(x=450,y=3,height=33)
        
        self.hover(self.btn)
        

        self.is_recording = False
        self.writer = None

    def activer_camera(self):
        self.statue=True
        self.update_video()

    def update_video(self):
        ret, frame = self.vid.read()

        if ret:
            # Appliquer le filtre si nécessaire
            if hasattr(self, 'filter') and self.filter:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convertir l'image BGR en RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            

            # Convertir le frame en image utilisable dans Tkinter
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Afficher l'image dans le canvas
            self.canvas.create_image(200, 40, anchor=NW, image=img_tk)

            # Maintenir la référence de l'image
            self.canvas.img_tk = img_tk

            # Mettre à jour le flux vidéo
            self.canvas.after(10, self.update_video)


    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.writer:
            self.writer.release()
            
    def on_enter(self,event):
        event.widget.config(background="#3CB371", fg="black") 


    def on_leave(self,event):
        event.widget.config(background="green", fg="white")  
        
    def hover(self,btn):
        
        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)