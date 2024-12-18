"""Contrôleur principal de l'application."""
from models.database import DatabaseModel
from models.face_recognition_model import FaceRecognitionModel
import os
import urllib.request


class MainController:
    """Gère la logique principale de l'application."""

    def __init__(self, view):
        """Initialise le contrôleur avec la vue associée."""
        self.view = view
        self.db_model = DatabaseModel()
        self.face_model = FaceRecognitionModel()
        self.current_employee = None

        # Créer le répertoire des visages s'il n'existe pas
        self.faces_dir = os.path.join(os.path.dirname(__file__), '..', 'faces')
        os.makedirs(self.faces_dir, exist_ok=True)

        # Charger les visages des employés
        self.load_employee_faces()

    def load_employee_faces(self):
        """Charge les visages des employés depuis la base de données."""
        employees = self.db_model.get_all_employees()
        print(f"Found {len(employees)} employees in database")
        print("\nEmployees in database:")
        for emp in employees:
            print(f"ID: {emp['id_employee']}, "
                  f"Name: {emp['first_name']} {emp['last_name']}")

        for employee in employees:
            if employee['photo_url']:
                try:
                    photo_filename = f"{employee['id_employee']}.jpg"
                    photo_path = os.path.join(self.faces_dir, photo_filename)
                    print(f"Processing employee {employee['id_employee']}, "
                          f"photo path: {photo_path}")

                    if not os.path.exists(photo_path):
                        print(f"Downloading photo for employee "
                              f"{employee['id_employee']}")
                        urllib.request.urlretrieve(employee['photo_url'],
                                                   photo_path)
                        print(f"Photo downloaded successfully to {photo_path}")
                    else:
                        print(f"Photo already exists at {photo_path}")
                except Exception as e:
                    print(f"Error downloading photo for employee "
                          f"{employee['id_employee']}: {e}")
            else:
                print(f"No photo URL for employee {employee['id_employee']}")

        if os.path.exists(self.faces_dir):
            print(f"\nFiles in faces directory: {os.listdir(self.faces_dir)}")
            print(f"Loading faces from directory: {self.faces_dir}")
            self.face_model.load_known_faces(self.faces_dir)
        else:
            print("Faces directory does not exist!")

    def start_camera(self):
        """Démarre le flux de la caméra."""
        self.face_model.initialize_camera()
        self.update_camera_feed()

    def update_camera_feed(self):
        """Met à jour le flux de la caméra dans la vue."""
        try:
            frame = self.face_model.capture_frame()
            self.view.update_camera_feed(frame)
            self.view.after(10, self.update_camera_feed)
        except Exception as e:
            print(f"Camera error: {e}")

    def capture_and_verify(self):
        """Capture un cadre et vérifie l'identité."""
        try:
            frame = self.face_model.capture_frame()
            employee_id = self.face_model.identify_face(frame)
            print(f"Face recognition result: {employee_id}")

            if employee_id:
                print("Face recognized, verifying with database...")
                employee_data = self.db_model.verify_employee(employee_id)
                print(f"Database verification result: {employee_data}")

                if employee_data:
                    print("Employee verified successfully!")
                    self.current_employee = employee_data
                    self.view.show_equipment_screen()
                    return True
                else:
                    print("Employee not found in database")
            else:
                print("Face not recognized")

            self.view.show_access_denied()
            return False
        except Exception as e:
            print(f"Error during face capture and verification: {e}")
            self.view.show_access_denied()
            return False

    def get_equipment_list(self):
        """Retourne la liste de tout l'équipement."""
        return self.db_model.get_all_equipment()

    def get_employee_equipment(self):
        """Retourne l'équipement assigné à l'employé actuel."""
        if self.current_employee:
            return self.db_model.get_employee_equipment(
                self.current_employee['id_employee']
            )
        return []

    def assign_equipment(self, equipment_id):
        """Assigne un équipement à l'employé actuel."""
        if not self.current_employee:
            print("No employee selected")
            return False
        print(f"Assigning equipment {equipment_id} to employee "
              f"{self.current_employee['id_employee']}")
        return self.db_model.assign_equipment(
            self.current_employee['id_employee'],
            equipment_id
        )

    def unassign_equipment(self, equipment_id):
        """Retire un équipement de l'employé actuel."""
        if not self.current_employee:
            print("No employee selected")
            return False
        print(f"Unassigning equipment {equipment_id} from employee "
              f"{self.current_employee['id_employee']}")
        return self.db_model.unassign_equipment(
            self.current_employee['id_employee'],
            equipment_id
        )

    def save_equipment_changes(self, final_equipment_state):
        """Sauvegarde les changements d'équipement dans la base de données."""
        if not self.current_employee:
            return

        current_equipment = self.get_employee_equipment()
        current_equipment_ids = {eq['id_equipment'] for eq in current_equipment}

        for equipment_id, is_checked in final_equipment_state.items():
            if is_checked and equipment_id not in current_equipment_ids:
                self.assign_equipment(equipment_id)
            elif not is_checked and equipment_id in current_equipment_ids:
                self.unassign_equipment(equipment_id)

    def cleanup(self):
        """Nettoie les ressources."""
        self.face_model.release_camera()
