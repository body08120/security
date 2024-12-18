# Importation des bibliothèques nécessaires pour l'interface graphique et le traitement d'images
import tkinter as tk  # Importation de la bibliothèque tkinter pour créer des interfaces graphiques

from tkinter import ttk, messagebox  # Importation des modules ttk pour des widgets stylisés et messagebox pour les dialogues

import cv2  # Importation de la bibliothèque OpenCV pour le traitement d'images

from PIL import Image, ImageTk  # Importation de PIL pour la manipulation d'images

import urllib.request  # Importation pour faire des requêtes HTTP

from io import BytesIO  # Importation pour gérer les flux de bytes

import os  # Importation pour interagir avec le système d'exploitation



# Définition de la classe principale de l'interface graphique

class MainView(tk.Tk):

    def __init__(self):

        # Appel du constructeur de la classe parent (tk.Tk)

        super().__init__()



        # Configuration de la fenêtre principale

        self.title("Système de Contrôle d'Accès")  # Titre de la fenêtre

        self.configure(bg="#F2F2F2")  # Couleur de fond de la fenêtre

        

        # Configuration de l'écran

        # self.state('zoomed')  # Décommenter pour maximiser la fenêtre à l'ouverture

        self.geometry("800x480")  # Définition de la taille de la fenêtre

        self.resizable(False, False)  # Désactiver le redimensionnement de la fenêtre

        

        # Configuration du style

        self.style = ttk.Style()  # Création d'un objet Style pour personnaliser les widgets

        

        # Configuration du style des cases à cocher

        self.style.configure(

            "Custom.TCheckbutton",

            background="#F2F2F2",  # Couleur de fond

            foreground="#020202",  # Couleur du texte

            font=("Roboto", 11)  # Police et taille du texte

        )

        

        # Configuration du style des titres

        self.style.configure(

            "Title.TLabel",

            background="#F2F2F2",  # Couleur de fond

            foreground="#379EC1",  # Couleur du texte

            font=("Roboto", 14, "bold")  # Police, taille et style du texte

        )

        

        # Configuration du style des labels normaux

        self.style.configure(

            "TLabel",

            background="#F2F2F2",  # Couleur de fond

            foreground="#020202",  # Couleur du texte

            font=("Roboto", 11)  # Police et taille du texte

        )

        

        # Configuration du style des frames

        self.style.configure(

            "TFrame",

            background="#F2F2F2"  # Couleur de fond

        )



        # Conteneur principal

        self.main_container = ttk.Frame(self)  # Création d'un frame pour le contenu principal

        self.main_container.pack(fill=tk.BOTH, expand=True)  # Remplir le conteneur principal



        # Cadre pour la caméra

        self.camera_frame = ttk.Frame(self.main_container)  # Création d'un frame pour la caméra

        self.camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Remplir le côté gauche



        self.camera_label = ttk.Label(self.camera_frame)  # Label pour afficher le flux vidéo de la caméra

        self.camera_label.pack(fill=tk.BOTH, expand=True)  # Remplir le cadre de la caméra



        # Cadre de contrôle

        self.control_frame = ttk.Frame(self.main_container)  # Création d'un frame pour les contrôles

        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)  # Remplir le côté droit



        # Style personnalisé pour les boutons

        button_style = {

            'bg': '#379EC1',  # Couleur de fond

            'fg': '#F2F2F2',  # Couleur du texte

            'font': ('Roboto', 11, 'bold'),  # Police et taille du texte

            'relief': 'flat',  # Style de bord

            'padx': 20,  # Espacement horizontal

            'pady': 10,  # Espacement vertical

            'cursor': 'hand2'  # Curseur main au survol

        }



        # Bouton de capture

        self.capture_button = tk.Button(

            self.control_frame,

            text="S'identifier",  # Texte affiché sur le bouton

            command=self.on_capture,  # Fonction appelée lors du clic

            **button_style  # Application du style personnalisé

        )

        self.capture_button.pack(pady=20, padx=10)  # Ajout du bouton au cadre de contrôle

        

        # Ajouter les événements de survol pour le bouton

        self.capture_button.bind('<Enter>', lambda e: e.widget.configure(bg='#2b7e9a'))  # Changer la couleur de fond au survol

        self.capture_button.bind('<Leave>', lambda e: e.widget.configure(bg='#379EC1'))  # Rétablir la couleur de fond à la sortie



        # Cadre pour l'équipement (initialement caché)

        self.equipment_frame = ttk.Frame(self)  # Création d'un frame pour gérer l'équipement

        self.equipment_checkboxes = {}  # Dictionnaire pour stocker les cases à cocher de l'équipement

        

        # Configuration de la mise en page du cadre d'équipement

        self.equipment_frame.columnconfigure(2, weight=2)  # La colonne du milieu s'étend

        

        # Bouton de retour (gauche)

        self.back_button = tk.Button(

            self.equipment_frame,

            text="Retour",  # Texte affiché sur le bouton

            command=self.show_main_screen,  # Fonction appelée lors du clic

            **button_style  # Application du style personnalisé

        )

        self.back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")  # Ajout du bouton au cadre d'équipement

        

        # Ajouter les événements de survol pour le bouton de retour

        self.back_button.bind('<Enter>', lambda e: e.widget.configure(bg='#2b7e9a'))  # Changer la couleur de fond au survol

        self.back_button.bind('<Leave>', lambda e: e.widget.configure(bg='#379EC1'))  # Rétablir la couleur de fond à la sortie



        # Conteneur de la liste d'équipement (milieu)

        self.equipment_list_frame = ttk.Frame(self.equipment_frame)  # Création d'un frame pour la liste d'équipement

        self.equipment_list_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nw")  # Ajout du cadre à la grille

        

        # Conteneur pour la photo de l'employé (en haut à droite)

        self.photo_frame = ttk.Frame(self.equipment_frame)  # Création d'un frame pour la photo de l'employé

        self.photo_frame.grid(row=0, column=2, padx=20, pady=20, sticky="ne")  # Ajout du cadre à la grille

        

        self.employee_photo_label = ttk.Label(self.photo_frame)  # Label pour afficher la photo de l'employé

        self.employee_photo_label.pack()  # Ajout du label au cadre de la photo



    def update_camera_feed(self, frame):

        """Mise à jour de l'affichage du flux de la caméra"""

        # Ajuster la taille du cadre de la caméra

        frame = cv2.resize(frame, (640, 470))  # Ajuster la hauteur à 470 pixels

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir l'image de BGR à RGB

        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))  # Convertir le tableau d'images en PhotoImage

        self.camera_label.configure(image=photo)  # Mettre à jour le label de la caméra avec la nouvelle image

        self.camera_label.image = photo  # Garder une référence à l'image pour éviter qu'elle soit détruite



    def show_equipment_screen(self):

        """Afficher l'écran de gestion de l'équipement"""

        self.main_container.pack_forget()  # Cacher le conteneur principal

        self.equipment_frame.pack(fill=tk.BOTH, expand=True)  # Afficher le cadre d'équipement



        # Effacer les cases à cocher existantes

        for widget in self.equipment_list_frame.winfo_children():

            widget.destroy()  # Détruire les widgets enfants dans la liste d'équipement

        self.equipment_checkboxes.clear()  # Réinitialiser le dictionnaire des cases à cocher



        # Effacer les labels existants dans le cadre de la photo (y compris les labels de nom)

        for widget in self.photo_frame.winfo_children():

            widget.destroy()  # Détruire les widgets enfants dans le cadre de la photo



        # Liste d'équipement

        equipment_list = self.controller.get_equipment_list()  # Récupérer la liste des équipements

        assigned_equipment = self.controller.get_employee_equipment()  # Récupérer l'équipement assigné à l'employé

        assigned_ids = [eq['id_equipment'] for eq in assigned_equipment]  # Extraire les IDs des équipements assignés



        # Créer un widget Canvas et une barre de défilement

        canvas = tk.Canvas(self.equipment_list_frame, bg="#F2F2F2", height=450)  # Définir la hauteur à 450 pixels

        scrollbar = ttk.Scrollbar(self.equipment_list_frame, orient="vertical", command=canvas.yview)  # Barre de défilement verticale

        canvas.configure(yscrollcommand=scrollbar.set)  # Lier la barre de défilement au canvas



        # Créer un cadre pour contenir les cases à cocher à l'intérieur du canvas

        scrollable_frame = ttk.Frame(canvas, style="TFrame")  # Cadre défilable



        # Ajouter le cadre défilable au canvas

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  # Créer une fenêtre dans le canvas



        # Configurer la région de défilement

        scrollable_frame.bind(

            "<Configure>",

            lambda e: canvas.configure(

                scrollregion=canvas.bbox("all")  # Définir la région de défilement pour inclure tous les widgets

            )

        )



        # Utiliser la grille pour placer le canvas et la barre de défilement

        canvas.grid(row=0, column=0, sticky="nsew")  # Placer le canvas

        scrollbar.grid(row=0, column=1, sticky="ns")  # Placer la barre de défilement



        # Assurer que le cadre principal utilise une mise en page en grille pour remplir toute la fenêtre

        self.equipment_list_frame.grid_columnconfigure(0, weight=1)  # Configurer la colonne pour s'étendre

        self.equipment_list_frame.grid_rowconfigure(0, weight=1)  # Configurer la ligne pour s'étendre



        # Titre pour la liste d'équipement

        ttk.Label(

            scrollable_frame,

            text="Gestion du Matériel",  # Texte du titre

            style="Title.TLabel"  # Style du titre

        ).pack(anchor="w", pady=(0, 20))  # Placer le titre dans le cadre défilable



        # Cases à cocher pour l'équipement

        for equipment in equipment_list:

            var = tk.BooleanVar(value=equipment['id_equipment'] in assigned_ids)  # Variable pour la case à cocher

            

            # Ajouter la vérification et désactiver si la valeur est <= 0

            if equipment['quantity_equipment'] <= 0:  # Vérifier la quantité dans la base de données

                state = 'disabled'  # Désactiver la case à cocher si la quantité est nulle ou négative

            else:

                state = 'normal'  # Activer la case à cocher si la quantité est positive

            

            cb = ttk.Checkbutton(

                scrollable_frame,

                text=equipment['equipment_name'],  # Texte affiché sur la case à cocher

                variable=var,  # Variable associée à la case à cocher

                style="Custom.TCheckbutton",  # Style personnalisé

                command=lambda e=equipment, v=var: self.on_equipment_toggle(e, v),  # Fonction appelée lors du changement d'état

                state=state  # Désactiver la case à cocher si la condition est remplie

            )

            cb.pack(anchor="w", pady=5)  # Placer la case à cocher

            self.equipment_checkboxes[equipment['id_equipment']] = var  # Stocker la variable de la case à cocher



        # Charger et afficher la photo et le nom de l'employé

        if self.controller.current_employee and self.controller.current_employee['photo_url']:  # Vérifier si l'employé actuel a une photo

            try:

                # Construire le chemin absolu vers la photo

                photo_path = os.path.join(

                    os.path.dirname(__file__),  # Répertoire du fichier actuel

                    '..',  # Remonter d'un niveau

                    self.controller.current_employee['photo_url']  # URL de la photo de l'employé

                )

                

                # Charger l'image depuis le fichier local

                image = Image.open(photo_path)  # Ouvrir l'image

                image = image.resize((150, 150), Image.Resampling.LANCZOS)  # Redimensionner l'image

                

                # Convertir en PhotoImage

                photo = ImageTk.PhotoImage(image)  # Convertir l'image en PhotoImage

                

                # Créer et afficher l'image

                self.employee_photo_label = ttk.Label(self.photo_frame, image=photo)  # Créer un label pour la photo

                self.employee_photo_label.image = photo  # Garder une référence à l'image pour éviter qu'elle soit détruite

                self.employee_photo_label.pack()  # Placer le label

                

                # Ajouter un label pour afficher le nom et prénom sous la photo

                employee_name = f"{self.controller.current_employee['first_name']} {self.controller.current_employee['last_name']}"  # Construire le nom complet

                self.employee_name_label = ttk.Label(self.photo_frame, text=employee_name, style="TLabel")  # Créer un label pour le nom

                self.employee_name_label.pack()  # Placer le label

            except Exception as e:

                print(f"Error loading employee photo: {e}")  # Afficher une erreur si le chargement échoue



    def show_main_screen(self):

        """Return to the main screen and save equipment changes"""

        # Récupérer l'état final des équipements

        final_equipment_state = {id_equipment: var.get()  # Récupérer l'état de chaque case à cocher

                               for id_equipment, var in self.equipment_checkboxes.items()}

        

        # Sauvegarder les changements via le contrôleur

        self.controller.save_equipment_changes(final_equipment_state)  # Appeler la méthode pour sauvegarder les changements

        

        # Afficher un message de confirmation

        messagebox.showinfo("Succès", "Les changements ont été enregistrés avec succès")  # Afficher une boîte de message

        

        # Retour à l'écran principal

        self.equipment_frame.pack_forget()  # Cacher le cadre d'équipement

        self.main_container.pack(fill=tk.BOTH, expand=True)  # Afficher le conteneur principal



    def show_access_denied(self):

        """Show access denied message"""

        messagebox.showerror(

            "Accès Refusé",  # Titre de la boîte de message

            "Identification échouée. Accès non autorisé."  # Message d'erreur

        )



    def on_equipment_toggle(self, equipment, var):

        """Handle equipment checkbox toggle"""

        if var.get():  # Vérifier si la case à cocher est activée

            self.controller.assign_equipment(equipment['id_equipment'])  # Assigner l'équipement

        else:

            self.controller.unassign_equipment(equipment['id_equipment'])  # Désassigner l'équipement



    def on_capture(self):

        """Handle photo capture button click"""

        self.controller.capture_and_verify()  # Appeler la méthode pour capturer et vérifier l'identité



    def set_controller(self, controller):

        """Set the controller for this view"""

        self.controller = controller  # Définir le contrôleur pour la vue