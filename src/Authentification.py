from tkinter import *
import mysql.connector
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from main import main
from db_connection import get_connection
from pygame import mixer

# Fonction principale de Login
class Login:
    
    def __init__(self):
        
        self.varia=0
        
        self.root = Tk()
        self.root.title("S'Authentification")
        self.root.geometry("1000x540+260+140")
        icon_path = os.path.join(os.path.dirname(__file__), "../images/Logo.ico")
        self.root.iconbitmap(icon_path)
        self.root.resizable(False, False)
        self.root.configure(background="#0071BC", bd=3, relief=GROOVE)
        
        mixer.init()
        # l'ajoute de ces deux ligne pour eviter le retard de clique au niveau des boutton
        mixer.music.load(".\\Sound\\click.ogg")  

        bgiconUserimg = Image.open(".\\images\\Logo.png")
        bgiconUserimg = bgiconUserimg.resize((500, 540))
        bgiconUserPhoto = ImageTk.PhotoImage(bgiconUserimg)

        # Affichage de l'image
        bg_label = Label(self.root, image=bgiconUserPhoto, bd=3, relief=GROOVE)
        bg_label.image = bgiconUserPhoto  # Garder une référence à l'image
        bg_label.pack(side="left")

        # Titre
        lbltitre = Label(self.root, bd=4, relief=GROOVE, text="Authentification", font=("Times New Roman", 25), bg='#F7941D', fg='#FFFAFA')
        lbltitre.place(width=995, height=70)

        image_path = ".\\images\\username.jpg"
        bgiconnameimg = Image.open(image_path)
        bgiconnameimg = bgiconnameimg.resize((30, 30))
        bgiconnamePhoto = ImageTk.PhotoImage(bgiconnameimg)
        Label(self.root, image=bgiconnamePhoto, bd=3, relief=GROOVE).place(x=632, y=230, width=30, height=30)

        Label(self.root, text="Societe :", font=("Times New Roman", 18), background="#0071BC", fg='#FFFAFA').place(x=666, y=180, width=150)
        txtnomUtilisateur = Entry(self.root, bd=3, relief=GROOVE, font=('Consolas', 16))
        txtnomUtilisateur.place(x=660, y=230, width=200, height=30)

        image_path = '.\\images\\password.jpg'
        bgiconPasswordimg = Image.open(image_path)
        bgiconPasswordimg = bgiconPasswordimg.resize((30, 30))
        bgiconPasswordPhoto = ImageTk.PhotoImage(bgiconPasswordimg)

        Label(self.root, image=bgiconPasswordPhoto, bd=3, relief=GROOVE).place(x=632, y=330, width=30, height=30)

        # Initialisation de la variable show_password à l'intérieur de Login()
        show_password = [True]  # Utilisation d'une liste pour conserver la référence mutable

        # Fonction pour basculer l'affichage du mot de passe
        def toggle_password():
            mixer.music.load(".\\Sound\\click.ogg")  
            mixer.music.play()
            if show_password[0]:  # Accéder à l'état depuis la liste
                txtmdp.config(show='')  # Affiche le texte du mot de passe
                show_password[0] = False
                eye_button.config(image=eye_open)  # Change l'icône à l'œil ouvert
            else:
                txtmdp.config(show='*')  # Masque le texte avec des astérisques
                show_password[0] = True
                eye_button.config(image=eye_closed)  # Change l'icône à l'œil fermé

        # Label et champ de texte pour le mot de passe
        Label(self.root, text="Password :", font=("Times New Roman", 18), background="#0071BC", fg="white").place(x=666, y=280, width=150)
        txtmdp = Entry(self.root, show='*', bd=3, relief=GROOVE, font=('Consolas', 16))
        txtmdp.place(x=660, y=330, width=200, height=30)

        # Utilisation du module os pour obtenir les chemins absolus des images
        eye_closed_path = '.\\images\\eye_closed.png'
        eye_open_path = '.\\images\\eye_open.png'

        eye_closed_img = Image.open(eye_closed_path)
        eye_closed = ImageTk.PhotoImage(eye_closed_img.resize((30, 30)))

        eye_open_img = Image.open(eye_open_path)
        eye_open = ImageTk.PhotoImage(eye_open_img.resize((30, 30)))

        # Bouton pour basculer l'affichage du mot de passe
        eye_button = Button(self.root, image=eye_closed, command=toggle_password, bd=0, bg="#0071BC")
        eye_button.place(x=870, y=330, width=30, height=30)
                    
        
        def hover(btn):
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        def on_enter(event):
            event.widget.config(bg='white', fg='green')  # Change la couleur quand la souris entre

        def on_leave(event):
            event.widget.config(bg='green', fg='white')  # Réinitialise la couleur quand la souris sort
        
        def Seconnecter():
            
            mixer.music.load(".\\Sound\\click.ogg")  
            mixer.music.play()
            
            surnom = txtnomUtilisateur.get()
            mdp = txtmdp.get()

            if surnom == "" or mdp == "":
                messagebox.showerror("Erreur", "Remplir tous les champs")
            else:
                try:
                    # Connexion à la base de données
                    mabase = get_connection()
                    curs = mabase.cursor()

                    # Vérifier les identifiants
                    query = "SELECT password FROM admines WHERE societe = %s"
                    curs.execute(query, (surnom,))
                    user_data = curs.fetchone()

                    if user_data:
                        stored_password = user_data[0]

                        # Comparer les mots de passe en texte brut
                        if mdp == stored_password:
                            self.root.destroy()  # Ferme la fenêtre actuelle
                            main()
                            
                        else:
                            messagebox.showerror("Erreur", "Mot de passe incorrect.")
                    else:
                        messagebox.showerror("Erreur", "Nom d'utilisateur ou société incorrect.")

                except mysql.connector.Error as e:
                    messagebox.showerror("Erreur", f"Erreur de connexion au serveur : {str(e)}")

                finally:
                    if curs:
                        curs.close()
                    if mabase.is_connected():
                        mabase.close()


        # Fonction pour envoyer l'email de réinitialisation

        # Fonction de mot de passe oublié
        def forgot_password():
            
            self.root.destroy()
            fnt = Tk()
            fnt.title("Mot de Pass Obliér ")
            fnt.geometry("500x540+510+140")
            icon_path = os.path.join(os.path.dirname(__file__), "../images/Logo.ico")
            fnt.iconbitmap(icon_path)
            fnt.resizable(False, False)
            fnt.configure(background="#0071BC", bd=3, relief=GROOVE)
            # Titre
            lbltitre = Label(fnt, bd=4, relief=GROOVE, text="Forgot Password ", font=("Times New Roman", 25), bg='#F7941D', fg='White')
            lbltitre.place(width=495, height=70)
            
            email_label=Label(fnt, text="Entrer votre Email :", font=("Times New Roman", 15), background="#0071BC", fg='White')
            email_label.place(x=167, y=180)
            email_entry = Entry(fnt, bd=3, relief=GROOVE, font=('Consolas', 15))
            email_entry.place(x=100, y=230, width=300, height=30)

            def check_email_in_database(email):
                    connection = get_connection()
                    cursor = connection.cursor()
                    # Requête SQL pour vérifier si l'email existe dans la table utilisateur
                    query = "SELECT * FROM admines WHERE Email = %s"
                    cursor.execute(query, (email,))
                    result = cursor.fetchone()  # Consommer le résultat
                    return result is not None  # Retourne True si l'email est trouvé, sinon False
            

            def ChoiCode():
                mixer.music.load(".\\Sound\\click.ogg")  
                mixer.music.play()
                user_email = email_entry.get()
                
                # Vérification de l'email dans la base de données
                if user_email:
                    if check_email_in_database(user_email):  # Vérifie si l'email est dans la base de données
                        reset_code = randint(100000, 999999)
                        send_recovery_email(user_email, reset_code)
                        fnt.destroy()
                        if self.varia == 0:
                           verification_window(user_email, reset_code)
                        elif self.varia == 1 :
                            Login()
                        
                    else:
                        messagebox.showerror("Erreur", "Cet email n'est pas enregistré dans notre système.")
                        
                        
                else:
                    messagebox.showerror("Erreur", "Veuillez entrer un email valide.")

            login_button = Button(fnt, bd=3, relief=GROOVE, font=("Times New Roman", 15), background="green", fg="white", text="Envoyer", command=ChoiCode)
            login_button.place(x=100, y=330, width=200, height=40)
            hover(login_button)
            
            def retour():
                mixer.music.load(".\\Sound\\click.ogg")  
                mixer.music.play()
                fnt.destroy()
                Login()
                    
            image_path = '.\\images\\retour.jpeg'
            iconRetour = Image.open(image_path)
            iconRetour = iconRetour.resize((60, 40))
            iconPhoto = ImageTk.PhotoImage(iconRetour)
                    
            Btn1 = Button(fnt, image=iconPhoto, command=retour)
            Btn1.place(x=340, y=330, width=60, height=40)
            
            fnt.mainloop()
            
        def send_recovery_email(to_email, reset_code):
            try:
                from_email = "anwar1bahida1@gmail.com"
                from_password = "qohlwbpqwmticgok"
                subject = "Récupération de mot de passe"

                message = MIMEMultipart()
                message["From"] = from_email
                message["To"] = to_email
                message["Subject"] = subject

                body = f"Bonjour,\n\nVoici votre code de réinitialisation : {reset_code}"
                message.attach(MIMEText(body, "plain"))

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(from_email, from_password)

                server.sendmail(from_email, to_email, message.as_string())
                server.quit()

                messagebox.showinfo("Succès", "Email de récupération envoyé avec succès !")

            except Exception as e:
                ok = messagebox.showerror("Erreur", f"Veuillez vérifier votre Connexion Internet")
                if ok : self.varia=1
        # Fonction de vérification du code de réinitialisation
        def verification_window(user_email,reset_code):
            fnt1 = Tk()
            fnt1.title("Recevoir Code")
            fnt1.geometry("500x540+510+140")
            icon_path = os.path.join(os.path.dirname(__file__), "../images/Logo.ico")
            fnt1.iconbitmap(icon_path)

            fnt1.resizable(False, False)
            fnt1.configure(background="#0071BC", bd=3, relief=GROOVE)
            
            lbltitre = Label(fnt1, bd=4, relief=GROOVE, text="Code Reçu", font=("Times New Roman", 25), bg='#F7941D', fg='#FFFAFA')
            lbltitre.place(width=495, height=70)
            
            code_label = Label(fnt1, text="Entrer le Code reçu : ", font=("Times New Roman", 15), background="#0071BC", fg="black")
            code_label.place(x=170, y=180)
            code_entry = Entry(fnt1, bd=3, relief=GROOVE, font=('Consolas', 15))
            code_entry.place(x=100, y=230, width=300, height=30)

            def verification():
                mixer.music.load(".\\Sound\\click.ogg")  
                mixer.music.play()
                
                code_input = code_entry.get()

                # Vérifier si l'entrée est un entier positif pur
                if not code_input.isdigit():
                    messagebox.showerror("Erreur", "Le code doit contenir 6 chiffres.")
                    return

                # Vérifier si le code est correct
                if reset_code == int(code_input):
                    # Fermer la fenêtre actuelle
                    fnt1.destroy()
                    # Ouvrir la fenêtre pour entrer un nouveau mot de passe
                    reset_password_window(user_email)
                else:
                    messagebox.showerror("Erreur", "Code incorrect . Vérifiez votre boîte email.")


            validate_button = Button(fnt1, text="Vérifier",bd=3, relief=GROOVE, font=("Times New Roman", 15), background="green", fg="white", command=verification)
            validate_button.place(x=100, y=330, width=300, height=30)
            hover(validate_button)
            
        def reset_password_window(user_email):
            
            fnt2 = Tk()
            fnt2.title("Recevoir Code")
            fnt2.geometry("500x540+510+140")
            icon_path = os.path.join(os.path.dirname(__file__), "../images/Logo.ico")
            fnt2.iconbitmap(icon_path)

            fnt2.resizable(False, False)
            fnt2.configure(background="#0071BC", bd=3, relief=GROOVE)
            
            lbltitre = Label(fnt2, bd=4, relief=GROOVE, text="New Password", font=("Times New Roman", 25), bg='#F7941D', fg='#FFFAFA')
            lbltitre.place(width=495, height=70)

            # Labels et champs pour entrer le nouveau mot de passe
            new_password_label = Label(fnt2, text="Nouveau mot de passe", font=("Times New Roman", 15), background="#0071BC", fg='White')
            new_password_label.place(x=150, y=180)
            new_password_entry = Entry(fnt2, show="*",bd=3, relief=GROOVE, font=('Consolas', 15))
            new_password_entry.place(x=100, y=230, width=300, height=30)

            confirm_password_label = Label(fnt2, text="Confirmer le mot de passe", font=("Times New Roman", 15), background="#0071BC", fg='White')
            confirm_password_label.place(x=150, y=280)
            confirm_password_entry = Entry(fnt2, show="*",bd=3, relief=GROOVE, font=('Consolas', 15))
            confirm_password_entry.place(x=100, y=330, width=300, height=30)

            # Fonction pour mettre à jour le mot de passe dans la base de données
            def update_password():
                mixer.music.load(".\\Sound\\click.ogg")  
                mixer.music.play()
                
                new_password = new_password_entry.get()
                confirm_password = confirm_password_entry.get()

                if new_password == "" or confirm_password == "":
                    messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
                elif new_password != confirm_password:
                    messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                else:
                    try:
                        
                        # Connexion à la base de données pour mettre à jour le mot de passe
                        mabase = get_connection()
                        curs = mabase.cursor()

                        # Mettre à jour le mot de passe dans la base de données (utiliser un identifiant unique ou email)
                        update_query = "UPDATE admines SET password = %s WHERE Email = %s"
                        curs.execute(update_query, (new_password, user_email))  # Assure-toi que `user_email` est défini pour identifier l'utilisateur

                        mabase.commit()
                        messagebox.showinfo("Succès", "Mot de passe réinitialisé avec succès.")
                        
                        # Fermer la fenêtre de réinitialisation
                        fnt2.destroy()
                        # Relancer l'interface de connexion
                        Login()

                    except mysql.connector.Error as e:
                        messagebox.showerror("Erreur", f"Erreur de connexion à la base de données : {str(e)}")
                    finally:
                        if curs:
                            curs.close()
                        if mabase.is_connected():
                            mabase.close()

            # Bouton pour soumettre le nouveau mot de passe
            submit_button = Button(fnt2, text="Réinitialiser Password",bd=3, relief=GROOVE, font=("Times New Roman", 18), background="green", fg="white", command=update_password)
            submit_button.place(x=100, y=380, width=300, height=30)

        # Boutons de connexion et création de compte
        btnSeConnecter = Button(self.root, bd=3, relief=GROOVE, text="Se Connecter", font=("Times New Roman", 18), background="green", fg="white", command=Seconnecter)
        btnSeConnecter.place(x=645, y=390, width=200)
        
        hover(btnSeConnecter)
        
        forgot_password_label = Label(self.root, text="Mot de passe oublié ?", fg='White', cursor="hand2" ,bg='#0071BC')
        forgot_password_label.place(x=685, y=450)
        forgot_password_label.bind("<Button-1>", lambda e: forgot_password())
        
        
        # Ajout de la ligne sous le label
        canvas = Canvas(self.root, width=110, height=1, bg='#0071BC', highlightthickness=0)
        canvas.create_line(0, 0, 140, 0, fill="White")
        canvas.place(x=688, y=470)  # Position de la ligne sous le label

        self.root.mainloop()
    
Login()