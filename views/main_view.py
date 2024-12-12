import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import os

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Système de Contrôle d'Accès")
        self.configure(bg="#FFFFFF")
        
        # Configuration en plein écran
        self.state('zoomed')
        
        # Style configuration
        self.style = ttk.Style()
        
        # Style des cases à cocher
        self.style.configure(
            "Custom.TCheckbutton",
            background="#FFFFFF",
            foreground="#000000",
            font=("Roboto", 11)
        )
        
        # Style des titres
        self.style.configure(
            "Title.TLabel",
            background="#FFFFFF",
            foreground="#379EC1",
            font=("Roboto", 16, "bold")
        )
        
        # Style des labels normaux
        self.style.configure(
            "TLabel",
            background="#FFFFFF",
            foreground="#000000",
            font=("Roboto", 11)
        )
        
        # Style des frames
        self.style.configure(
            "TFrame",
            background="#FFFFFF"
        )

        # Main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Camera frame
        self.camera_frame = ttk.Frame(self.main_container)
        self.camera_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        # Control frame
        self.control_frame = ttk.Frame(self.main_container)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Style personnalisé pour les boutons
        button_style = {
            'bg': '#379EC1',
            'fg': '#FFFFFF',
            'font': ('Roboto', 12, 'bold'),
            'relief': 'flat',
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2'  # Curseur main au survol
        }

        self.capture_button = tk.Button(
            self.control_frame,
            text="S'identifier",
            command=self.on_capture,
            **button_style
        )
        self.capture_button.pack(pady=20, padx=10)
        
        # Ajouter les événements de survol
        self.capture_button.bind('<Enter>', lambda e: e.widget.configure(bg='#2b7e9a'))
        self.capture_button.bind('<Leave>', lambda e: e.widget.configure(bg='#379EC1'))

        # Equipment frame (initially hidden)
        self.equipment_frame = ttk.Frame(self)
        self.equipment_checkboxes = {}
        
        # Configure equipment frame layout
        self.equipment_frame.columnconfigure(1, weight=1)  # Middle column expands
        
        # Back button (left)
        self.back_button = tk.Button(
            self.equipment_frame,
            text="Validation",
            command=self.show_main_screen,
            **button_style
        )
        self.back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
        
        # Ajouter les événements de survol
        self.back_button.bind('<Enter>', lambda e: e.widget.configure(bg='#2b7e9a'))
        self.back_button.bind('<Leave>', lambda e: e.widget.configure(bg='#379EC1'))

        # Equipment list container (middle)
        self.equipment_list_frame = ttk.Frame(self.equipment_frame)
        self.equipment_list_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nw")
        
        # Employee photo container (top-right)
        self.photo_frame = ttk.Frame(self.equipment_frame)
        self.photo_frame.grid(row=0, column=2, padx=20, pady=20, sticky="ne")
        
        self.employee_photo_label = ttk.Label(self.photo_frame)
        self.employee_photo_label.pack()

    def update_camera_feed(self, frame):
        """Update the camera feed display"""
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.camera_label.configure(image=photo)
        self.camera_label.image = photo

    def show_equipment_screen(self):
        """Show the equipment management screen"""
        self.main_container.pack_forget()
        self.equipment_frame.pack(fill=tk.BOTH, expand=True)
        
        # Clear existing checkboxes
        for widget in self.equipment_list_frame.winfo_children():
            widget.destroy()
        self.equipment_checkboxes.clear()

        # Equipment list
        equipment_list = self.controller.get_equipment_list()
        assigned_equipment = self.controller.get_employee_equipment()
        assigned_ids = [eq['id_equipment'] for eq in assigned_equipment]

        # Title for equipment list
        ttk.Label(
            self.equipment_list_frame,
            text="Gestion du Matériel",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        # Equipment checkboxes
        for equipment in equipment_list:
            var = tk.BooleanVar(value=equipment['id_equipment'] in assigned_ids)
            cb = ttk.Checkbutton(
                self.equipment_list_frame,
                text=equipment['equipment_name'],
                variable=var,
                style="Custom.TCheckbutton",
                command=lambda e=equipment, v=var: self.on_equipment_toggle(e, v)
            )
            cb.pack(anchor="w", pady=5)
            self.equipment_checkboxes[equipment['id_equipment']] = var

        # Load and display employee photo
        if self.controller.current_employee and self.controller.current_employee['photo_url']:
            try:
                # Construire le chemin absolu vers la photo
                photo_path = os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    self.controller.current_employee['photo_url']
                )
                
                # Charger l'image depuis le fichier local
                image = Image.open(photo_path)
                
                # Resize to reasonable dimensions
                image = image.resize((150, 150), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Update label
                self.employee_photo_label.configure(image=photo)
                self.employee_photo_label.image = photo
            except Exception as e:
                print(f"Error loading employee photo: {e}")

    def show_main_screen(self):
        """Return to the main screen and save equipment changes"""
        # Récupérer l'état final des équipements
        final_equipment_state = {id_equipment: var.get() 
                               for id_equipment, var in self.equipment_checkboxes.items()}
        
        # Sauvegarder les changements via le contrôleur
        self.controller.save_equipment_changes(final_equipment_state)
        
        # Afficher un message de confirmation
        messagebox.showinfo("Succès", "Les changements ont été enregistrés avec succès")
        
        # Retour à l'écran principal
        self.equipment_frame.pack_forget()
        self.main_container.pack(fill=tk.BOTH, expand=True)

    def show_access_denied(self):
        """Show access denied message"""
        messagebox.showerror(
            "Accès Refusé",
            "Identification échouée. Accès non autorisé."
        )

    def on_equipment_toggle(self, equipment, var):
        """Handle equipment checkbox toggle"""
        if var.get():
            self.controller.assign_equipment(equipment['id_equipment'])
        else:
            self.controller.unassign_equipment(equipment['id_equipment'])

    def on_capture(self):
        """Handle photo capture button click"""
        self.controller.capture_and_verify()

    def set_controller(self, controller):
        """Set the controller for this view"""
        self.controller = controller
