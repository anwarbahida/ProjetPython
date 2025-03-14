from tkinter import ttk, messagebox, filedialog
from tkinter import *
from db_connection import get_connection
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from fpdf import FPDF
import io
from PIL import Image
import tempfile
import os
import matplotlib.pyplot as plt 
from tkcalendar  import Calendar
from pygame import mixer

class Rapport:
    def __init__(self, frm, frm1):
        self.frm = frm
        self.frm.config(bg="#e0e0e0")
        self.frm1 = frm1
        
        mixer.init()
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        
        self.create_widgets()
    
    def on_enter(self,event):
        event.widget.config(background="#3CB371", fg="black") 


    def on_leave(self,event):
        event.widget.config(background="green", fg="white")  
        
    def hover(self,btn):
        
        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)
    
    
    def create_widgets(self):
        titre=Label(self.frm1,text="Rapport Statistique",bg="gray",fg='white',font=("Consolas", 20))
        titre.place(x=400,y=30,width=300)

        # Zone d'affichage des statistiques
        self.stats_frame = Frame(self.frm, bg="#e0e0e0")
        self.stats_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Ajouter un champ de sélection de la date
        self.calendar_label = Label(self.frm, text="Sélectionner une date:", font=("consolas", 16), bg="#e0e0e0")
        self.calendar_label.place(x=70, y=230)

        self.cal = Calendar(self.frm, date_pattern='yyyy-mm-dd')
        self.cal.place(x=430, y=150)

        # Bouton pour générer le rapport
        btnGenRap = Button(self.frm, text="Générer Rapport", command=self.generate_report,background="green", fg="white", font=("Times New Roman", 15))
        btnGenRap.place(x=730, y=60, width=200)
        
        self.hover(btnGenRap)

        # Bouton pour télécharger le rapport PDF
        btnTeleRap = Button(self.frm, text="Télécharger PDF", command=self.export_to_pdf, background="#27D4FC", fg="black" , font=("Times New Roman", 15))
        btnTeleRap.place(x=730, y=120, width=200)
        
        self.hoverBlue(btnTeleRap)

    def on_enterBlue(self,event):
        event.widget.config(background="#27D4FC", fg="black") 


    def on_leaveBlue(self,event):
        event.widget.config(background="#0A82A0", fg="white")  
        
    def hoverBlue(self,btn):
        
        btn.bind("<Enter>", self.on_enterBlue)
        btn.bind("<Leave>", self.on_leaveBlue)
    
    def generate_report(self):
        
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        mixer.music.play()
        # Détruire le label du calendrier
        self.calendar_label.destroy()
        
        # Détruire le widget du calendrier
        self.cal.destroy()
        
        try:
            # Récupérer la date choisie dans le calendrier
            selected_date = self.cal.get_date()
            print(f"Date sélectionnée : {selected_date}")  # Afficher la date sélectionnée pour débogage

            # Connexion à la base de données
            conn = get_connection()
            cursor = conn.cursor()

            # Récupérer la date et les statistiques des employés présents et absents
            query_presence_date = """
                SELECT DISTINCT DATE(presence.date_time) AS date_presence
                FROM presence
                WHERE DATE(presence.date_time) = %s
            """
            query_present_employes = """
                SELECT COUNT(*) 
                FROM Employes 
                WHERE Employes.id IN (
                    SELECT presence.id_employe 
                    FROM presence 
                    WHERE DATE(presence.date_time) = %s
                )
            """
            query_absent_employes = """
                SELECT COUNT(*) 
                FROM Employes 
                WHERE Employes.id NOT IN (
                    SELECT presence.id_employe 
                    FROM presence 
                    WHERE DATE(presence.date_time) = %s
                )
            """

            # Récupérer la date de la présence
            cursor.execute(query_presence_date, (selected_date,))
            date_presence = cursor.fetchone()
            if not date_presence:
                messagebox.showwarning("Avertissement", "Aucune donnée trouvée pour la date sélectionnée.")
                return  # Si la date n'existe pas, arrêter l'exécution

            date_presence = date_presence[0]  # La date

            # Récupérer le nombre d'employés présents
            cursor.execute(query_present_employes, (selected_date,))
            total_present = cursor.fetchone()[0]
            

            # Récupérer le nombre d'employés absents
            cursor.execute(query_absent_employes, (selected_date,))
            total_absent = cursor.fetchone()[0]
            

            # Récupérer les postes les plus occupés
            query_postes = """
                SELECT post, COUNT(*) as count 
                FROM Employes 
                GROUP BY post 
                ORDER BY count DESC 
                LIMIT 5
            """
            cursor.execute(query_postes)
            postes_populaires = cursor.fetchall()
            

            # Nettoyer le cadre des statistiques
            for widget in self.stats_frame.winfo_children():
                widget.destroy()

            # Afficher la date et les statistiques des employés
            Label(self.stats_frame, text=f"Date de présence : {date_presence}", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(anchor="w", pady=5)
            Label(self.stats_frame, text=f"Présents : {total_present} | Absents : {total_absent}", font=("Arial", 14), bg="#e0e0e0").pack(anchor="w", pady=5)
            Label(self.stats_frame, text="Postes les plus occupés :", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(anchor="w", pady=5)
            for post, count in postes_populaires:
                Label(self.stats_frame, text=f"- {post} : {count} employés", font=("Arial", 14), bg="#e0e0e0").pack(anchor="w", padx=20)

            # Générer les graphiques
            self.plot_charts(total_present, total_absent, postes_populaires)

            # Stocker les données pour PDF
            self.report_data = {
                "date_presence": date_presence,
                "total_present": total_present,
                "total_absent": total_absent,
                "postes_populaires": postes_populaires
            }

            conn.close()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    

    def plot_charts(self, present, absent, postes_populaires):
        # Graphique en secteurs
        fig1 = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.pie([present, absent], labels=["Présents", "Absents"], autopct="%1.1f%%", startangle=90, colors=["green", "red"])
        ax1.set_title("Répartition par Statut")

        # Graphique en barres
        fig2 = Figure(figsize=(6, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        posts, counts = zip(*postes_populaires)
        ax2.bar(posts, counts, color="orange")
        ax2.set_title("Postes les Plus Occupés")
        ax2.set_ylabel("Nombre d'employés")

        # Afficher les graphiques
        canvas1 = FigureCanvasTkAgg(fig1, master=self.stats_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=LEFT, padx=10, pady=10)

        canvas2 = FigureCanvasTkAgg(fig2, master=self.stats_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=LEFT, padx=10, pady=10)

        # Sauvegarder les graphiques pour PDF
        self.graphic_data = {
            "pie_chart": self.figure_to_image(fig1),
            "bar_chart": self.figure_to_image(fig2)
        }

    @staticmethod
    def figure_to_image(figure):
        buf = io.BytesIO()
        figure.savefig(buf, format="png")
        buf.seek(0)
        return Image.open(buf)

 # Assurez-vous que Matplotlib est importé

    def export_to_pdf(self):
        
        mixer.music.load("C:\\Users\\HP\\ProjetPython\\Sound\\click.ogg")  
        mixer.music.play()
        if not hasattr(self, "report_data"):
            messagebox.showwarning("Attention", "Veuillez d'abord générer le rapport.")
            return

        # Créer un PDF avec une gestion améliorée de la mise en page
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.set_fill_color(173, 216, 230) 

        # Ajouter le titre du rapport
        self.add_title(pdf, "Rapport Statistique")

        # Ajouter les statistiques
        self.add_statistiques(pdf)

        # Ajouter des graphiques
        self.add_graphics(pdf)

        # Demander à l'utilisateur où enregistrer le fichier PDF
        self.save_pdf(pdf)

    def add_title(self, pdf, title):
        """
        Ajoute le titre du rapport au PDF
        """
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt=title, ln=True, align="C")
        pdf.ln(10)  # Ajouter un espace après le titre
        pdf.set_fill_color(0, 216, 230) 

    def add_statistiques(self, pdf):
        """
        Ajoute les statistiques (date, nombre de présents et absents, postes populaires) au PDF
        """
        pdf.set_font("Arial", size=12)
        
        # Ajouter la date de présence et les statistiques
        pdf.cell(0, 10, txt=f"Date de présence : {self.report_data['date_presence']}", ln=True)
        pdf.cell(0, 10, txt=f"Présents : {self.report_data['total_present']} | Absents : {self.report_data['total_absent']}", ln=True)
        pdf.ln(5)
        pdf.set_fill_color(173, 0 , 230) 

        # Ajouter les postes les plus occupés
        pdf.cell(0, 10, txt="Postes les plus occupés :", ln=True)
        for post, count in self.report_data['postes_populaires']:
            pdf.cell(0, 10, txt=f"- {post} : {count} employés", ln=True)

        pdf.ln(10)  # Ajouter un espace avant les graphiques

    def add_graphics(self, pdf):
        """
        Ajoute les graphiques générés avec Matplotlib au PDF
        """
        if hasattr(self, "graphic_data"):
            # Ajouter le graphique en secteurs (graphique en pie chart)
            self.add_image_to_pdf(pdf, self.graphic_data["pie_chart"])

            # Ajouter le graphique en barres (bar chart)
            self.add_image_to_pdf(pdf, self.graphic_data["bar_chart"])

    def add_image_to_pdf(self, pdf, img_data):
        """
        Ajoute une image au PDF en gérant le fichier temporaire
        """
        # Sauvegarder l'image dans un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_file_path = temp_file.name
            img_data.save(temp_file_path)

        # Ajouter l'image au PDF
        pdf.image(temp_file_path, x=10, y=None, w=170)
        pdf.ln(10)  # Ajouter un espace après l'image

        # Supprimer le fichier temporaire après l'ajout
        os.remove(temp_file_path)

    def save_pdf(self, pdf):
        """
        Sauvegarde le PDF dans un fichier choisi par l'utilisateur
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                pdf.output(file_path)
                messagebox.showinfo("Succès", "Le rapport a été enregistré avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'enregistrement du fichier : {e}")