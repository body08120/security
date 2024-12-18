# Importation des classes nécessaires pour le contrôle de l'application et la gestion des données
from models.database import DatabaseModel  # Importation de la classe DatabaseModel pour interagir avec la base de données
from models.face_recognition_model import FaceRecognitionModel  # Importation de la classe FaceRecognitionModel pour la reconnaissance faciale
import cv2  # Importation de la bibliothèque OpenCV pour le traitement d'images
import os  # Importation pour interagir avec le système d'exploitation
import urllib.request  # Importation pour faire des requêtes HTTP
from pathlib import Path  # Importation pour manipuler les chemins de fichiers

# Définition de la classe MainController pour gérer la logique de l'application
class MainController:
    def __init__(self, view):
        # Initialisation du contrôleur avec la vue associée
        self.view = view  # Stocker la référence à la vue
        self.db_model = DatabaseModel()  # Créer une instance du modèle de base de données
        self.face_model = FaceRecognitionModel()  # Créer une instance du modèle de reconnaissance faciale
        self.current_employee = None  # Variable pour stocker l'employé actuellement sélectionné
        
        # Créer un répertoire pour les visages s'il n'existe pas
        self.faces_dir = os.path.join(os.path.dirname(__file__), '..', 'faces')  # Chemin vers le répertoire des visages
        os.makedirs(self.faces_dir, exist_ok=True)  # Créer le répertoire s'il n'existe pas
        
        # Charger les visages des employés depuis la base de données
        self.load_employee_faces()  # Appeler la méthode pour charger les visages

    def load_employee_faces(self):
        """Charger les visages des employés à partir de la base de données"""
        employees = self.db_model.get_all_employees()  # Récupérer tous les employés de la base de données
        print(f"Found {len(employees)} employees in database")  # Afficher le nombre d'employés trouvés
        print("\nEmployees in database:")  # Afficher les employés dans la base de données
        for emp in employees:
            print(f"ID: {emp['id_employee']}, Name: {emp['first_name']} {emp['last_name']}")  # Afficher l'ID et le nom de chaque employé
        
        for employee in employees:  # Parcourir tous les employés
            if employee['photo_url']:  # Vérifier si l'employé a une URL de photo
                try:
                    # Créer le nom de fichier à partir de l'ID de l'employé
                    photo_filename = f"{employee['id_employee']}.jpg"  # Nom du fichier photo
                    photo_path = os.path.join(self.faces_dir, photo_filename)  # Chemin vers la photo
                    print(f"Processing employee {employee['id_employee']}, photo path: {photo_path}")  # Afficher le chemin de la photo
                    
                    # Télécharger la photo si elle n'existe pas
                    if not os.path.exists(photo_path):  # Vérifier si la photo existe déjà
                        print(f"Downloading photo for employee {employee['id_employee']}")  # Afficher un message de téléchargement
                        urllib.request.urlretrieve(employee['photo_url'], photo_path)  # Télécharger la photo
                        print(f"Photo downloaded successfully to {photo_path}")  # Afficher un message de succès
                    else:
                        print(f"Photo already exists at {photo_path}")  # Afficher un message si la photo existe déjà
                except Exception as e:  # Gérer les exceptions lors du téléchargement
                    print(f"Error downloading photo for employee {employee['id_employee']}: {e}")  # Afficher une erreur si le téléchargement échoue
            else:
                print(f"No photo URL for employee {employee['id_employee']}")  # Afficher un message si l'employé n'a pas de photo URL
        
        # Charger les visages après le téléchargement
        if os.path.exists(self.faces_dir):  # Vérifier si le répertoire des visages existe
            print(f"\nFiles in faces directory: {os.listdir(self.faces_dir)}")  # Afficher les fichiers dans le répertoire des visages
            print(f"Loading faces from directory: {self.faces_dir}")  # Afficher le répertoire de chargement des visages
            print(f"Directory contents: {os.listdir(self.faces_dir)}")  # Afficher le contenu du répertoire
            self.face_model.load_known_faces(self.faces_dir)  # Charger les visages connus à partir du répertoire
        else:
            print("Faces directory does not exist!")  # Afficher un message si le répertoire des visages n'existe pas

    def start_camera(self):
        """Démarrer le flux de la caméra"""
        self.face_model.initialize_camera()  # Initialiser la caméra
        self.update_camera_feed()  # Mettre à jour le flux de la caméra

    def update_camera_feed(self):
        """Mettre à jour le flux de la caméra dans la vue"""
        try:
            frame = self.face_model.capture_frame()  # Capturer un cadre de la caméra
            self.view.update_camera_feed(frame)  # Mettre à jour l'affichage de la caméra dans la vue
            self.view.after(10, self.update_camera_feed)  # Appeler cette méthode à nouveau après 10 ms
        except Exception as e:  # Gérer les exceptions lors de la mise à jour du flux
            print(f"Camera error: {e}")  # Afficher un message d'erreur

    def capture_and_verify(self):
        """Capturer un cadre et vérifier l'identité"""
        try:
            frame = self.face_model.capture_frame()  # Capturer un cadre de la caméra
            employee_id = self.face_model.identify_face(frame)  # Identifier le visage dans le cadre
            print(f"Face recognition result: {employee_id}")  # Afficher le résultat de la reconnaissance faciale
            
            if employee_id:  # Vérifier si un ID d'employé a été reconnu
                print("Face recognized, verifying with database...")  # Afficher un message de vérification
                employee_data = self.db_model.verify_employee(employee_id)  # Vérifier l'employé dans la base de données
                print(f"Database verification result: {employee_data}")  # Afficher le résultat de la vérification
                
                if employee_data:  # Vérifier si les données de l'employé ont été trouvées
                    print("Employee verified successfully!")  # Afficher un message de succès
                    self.current_employee = employee_data  # Stocker les données de l'employé actuel
                    self.view.show_equipment_screen()  # Afficher l'écran de gestion de l'équipement
                    return True  # Retourner True en cas de succès
                else:
                    print("Employee not found in database")  # Afficher un message si l'employé n'est pas trouvé
            else:
                print("Face not recognized")  # Afficher un message si le visage n'est pas reconnu
            
            self.view.show_access_denied()  # Afficher un message d'accès refusé
        except Exception as e:  # Gérer les exceptions lors de la capture et de la vérification
            print(f"Error during face capture and verification: {e}")  # Afficher le message d'erreur
            self.view.show_access_denied()  # Afficher un message d'accès refusé
            return False  # Retourner False en cas d'erreur

    def get_equipment_list(self):
        """Obtenir la liste de tout l'équipement"""
        return self.db_model.get_all_equipment()  # Retourner la liste de tous les équipements

    def get_employee_equipment(self):
        """Obtenir l'équipement assigné à l'employé actuel"""
        if self.current_employee:  # Vérifier si un employé est sélectionné
            return self.db_model.get_employee_equipment(self.current_employee['id_employee'])  # Retourner l'équipement assigné
        return []  # Retourner une liste vide si aucun employé n'est sélectionné

    def assign_equipment(self, equipment_id):
        """Assigner un équipement à l'employé actuel"""
        if not self.current_employee:  # Vérifier si un employé est sélectionné
            print("No employee selected")  # Afficher un message si aucun employé n'est sélectionné
            return False  # Retourner False si aucun employé n'est sélectionné
        print(f"Assigning equipment {equipment_id} to employee {self.current_employee['id_employee']}")  # Afficher un message d'assignation
        return self.db_model.assign_equipment(self.current_employee['id_employee'], equipment_id)  # Appeler la méthode pour assigner l'équipement

    def unassign_equipment(self, equipment_id):
        """Désassigner un équipement de l'employé actuel"""
        if not self.current_employee:  # Vérifier si un employé est sélectionné
            print("No employee selected")  # Afficher un message si aucun employé n'est sélectionné
            return False  # Retourner False si aucun employé n'est sélectionné
        print(f"Unassigning equipment {equipment_id} from employee {self.current_employee['id_employee']}")  # Afficher un message de désassignation
        return self.db_model.unassign_equipment(self.current_employee['id_employee'], equipment_id)  # Appeler la méthode pour désassigner l'équipement

    def save_equipment_changes(self, final_equipment_state):
        """Sauvegarder les changements d'équipement dans la base de données"""
        if not self.current_employee:  # Vérifier si un employé est sélectionné
            return  # Ne rien faire si aucun employé n'est sélectionné
            
        # Récupérer l'équipement actuellement assigné
        current_equipment = self.get_employee_equipment()  # Obtenir l'équipement actuellement assigné
        current_equipment_ids = {eq['id_equipment'] for eq in current_equipment}  # Extraire les IDs des équipements assignés
        
        # Pour chaque équipement dans l'état final
        for equipment_id, is_checked in final_equipment_state.items():  # Parcourir l'état final des équipements
            # Si coché et pas encore assigné -> assigner
            if is_checked and equipment_id not in current_equipment_ids:  # Vérifier si l'équipement doit être assigné
                self.assign_equipment(equipment_id)  # Appeler la méthode pour assigner l'équipement
                
            # Si décoché et actuellement assigné -> désassigner
            elif not is_checked and equipment_id in current_equipment_ids:  # Vérifier si l'équipement doit être désassigné
                self.unassign_equipment(equipment_id)  # Appeler la méthode pour désassigner l'équipement

    def cleanup(self):
        """Nettoyer les ressources"""
        self.face_model.release_camera()  # Libérer la caméra