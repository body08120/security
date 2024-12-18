# Importation des bibliothèques nécessaires pour la reconnaissance faciale et le traitement d'images
import face_recognition  # Importation de la bibliothèque pour la reconnaissance faciale
import cv2  # Importation de la bibliothèque OpenCV pour le traitement d'images
import numpy as np  # Importation de NumPy pour les opérations sur les tableaux
import os  # Importation pour interagir avec le système d'exploitation

# Définition de la classe FaceRecognitionModel pour gérer la reconnaissance faciale
class FaceRecognitionModel:
    def __init__(self):
        # Initialisation des listes pour stocker les encodages et les IDs des visages connus
        self.known_face_encodings = []  # Liste pour stocker les encodages des visages connus
        self.known_face_ids = []  # Liste pour stocker les IDs des visages connus
        self.camera = None  # Variable pour stocker l'objet de la caméra

    def load_known_faces(self, faces_directory):
        """Charger les visages connus à partir d'un répertoire"""
        print(f"\nStarting to load known faces from {faces_directory}")  # Afficher le répertoire de chargement
        for filename in os.listdir(faces_directory):  # Parcourir tous les fichiers dans le répertoire
            # Ignorer debug_capture.jpg
            if filename == 'debug_capture.jpg':
                continue  # Passer ce fichier
            
            if filename.endswith((".jpg", ".png")):  # Vérifier si le fichier est une image
                try:
                    employee_id = filename.split('.')[0]  # Extraire l'ID de l'employé à partir du nom de fichier
                    image_path = os.path.join(faces_directory, filename)  # Construire le chemin de l'image
                    print(f"Processing image: {image_path}")  # Afficher le chemin de l'image
                    
                    image = face_recognition.load_image_file(image_path)  # Charger l'image
                    print(f"Image loaded, shape: {image.shape}")  # Afficher la forme de l'image
                    
                    encodings = face_recognition.face_encodings(image)  # Obtenir les encodages du visage
                    if len(encodings) > 0:  # Vérifier si des encodages ont été trouvés
                        self.known_face_encodings.append(encodings[0])  # Ajouter l'encodage du visage à la liste
                        self.known_face_ids.append(employee_id)  # Ajouter l'ID de l'employé à la liste
                        print(f"Successfully encoded face for employee {employee_id}")  # Afficher un message de succès
                    else:
                        print(f"No face found in {filename}")  # Afficher un message si aucun visage n'est trouvé
                except Exception as e:
                    print(f"Error processing {filename}: {e}")  # Afficher une erreur lors du traitement de l'image
        
        print(f"Finished loading faces. Total faces loaded: {len(self.known_face_encodings)}")  # Afficher le nombre total de visages chargés

    def initialize_camera(self):
        """Initialiser la caméra"""
        self.camera = cv2.VideoCapture(0)  # Ouvrir la caméra par défaut
        if not self.camera.isOpened():  # Vérifier si la caméra s'est ouverte correctement
            raise Exception("Could not open camera")  # Lever une exception si la caméra ne peut pas être ouverte

    def capture_frame(self):
        """Capturer un cadre à partir de la caméra"""
        if self.camera is None:  # Vérifier si la caméra n'est pas initialisée
            self.initialize_camera()  # Initialiser la caméra si nécessaire
        ret, frame = self.camera.read()  # Lire un cadre de la caméra
        if not ret:  # Vérifier si la capture a réussi
            raise Exception("Could not capture frame")  # Lever une exception si la capture échoue
        return frame  # Retourner le cadre capturé

    def identify_face(self, frame):
        """Identifier un visage dans le cadre donné"""
        try:
            # Convertir BGR en RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir le cadre de BGR à RGB
            print("\nStarting face identification...")  # Afficher un message de début d'identification
            print(f"Number of known faces: {len(self.known_face_encodings)}")  # Afficher le nombre de visages connus
            
            # Trouver les visages dans le cadre
            face_locations = face_recognition.face_locations(rgb_frame)  # Localiser les visages dans le cadre
            if not face_locations:  # Vérifier si aucun visage n'est détecté
                print("No face detected in frame")  # Afficher un message si aucun visage n'est détecté
                return None  # Retourner None si aucun visage n'est trouvé

            print(f"Found {len(face_locations)} faces in frame")  # Afficher le nombre de visages trouvés
            
            # Obtenir les encodages des visages
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)  # Obtenir les encodages des visages détectés
            
            if not face_encodings:  # Vérifier si aucun encodage n'a été trouvé
                print("Could not encode face")  # Afficher un message si l'encodage échoue
                return None  # Retourner None si l'encodage échoue

            print(f"Successfully encoded {len(face_encodings)} faces from frame")  # Afficher le nombre de visages encodés

            for face_encoding in face_encodings:  # Parcourir tous les encodages de visages
                # Comparer avec les visages connus
                if len(self.known_face_encodings) > 0:  # Vérifier s'il y a des visages connus
                    # Calculer les distances faciales
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)  # Calculer les distances entre les visages
                    print(f"Face distances: {face_distances}")  # Afficher les distances faciales
                    
                    matches = face_recognition.compare_faces(  # Comparer les visages encodés avec les visages connus
                        self.known_face_encodings, 
                        face_encoding,
                        tolerance=0.7  # Augmenter la tolérance (défaut est 0.6)
                    )
                    
                    print(f"Matches results: {matches}")  # Afficher les résultats de la comparaison
                    
                    if True in matches:  # Vérifier si un match a été trouvé
                        first_match_index = matches.index(True)  # Obtenir l'index du premier match
                        matched_id = self.known_face_ids[first_match_index]  # Obtenir l'ID correspondant au match
                        print(f"Match found! Employee ID: {matched_id}")  # Afficher l'ID de l'employé correspondant
                        return matched_id  # Retourner l'ID de l'employé
                    else:
                        print("No matches found with known faces")  # Afficher un message si aucun match n'est trouvé
                else:
                    print("No known faces to compare with")  # Afficher un message si aucune face connue n'est disponible
            
            return None  # Retourner None si aucun match n'est trouvé
        except Exception as e:  # Gérer les exceptions lors de l'identification
            print(f"Error in face identification: {e}")  # Afficher le message d'erreur
            return None  # Retourner None en cas d'erreur

    def release_camera(self):
        """Libérer la caméra"""
        if self.camera is not None:  # Vérifier si la caméra est initialisée
            self.camera.release()  # Libérer la caméra
            self.camera = None  # Réinitialiser la variable de la caméra