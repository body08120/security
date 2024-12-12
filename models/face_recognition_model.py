import face_recognition
import cv2
import numpy as np
import os

class FaceRecognitionModel:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_ids = []
        self.camera = None

    def load_known_faces(self, faces_directory):
        """Load known faces from directory"""
        print(f"\nStarting to load known faces from {faces_directory}")
        for filename in os.listdir(faces_directory):
            # Ignore debug_capture.jpg
            if filename == 'debug_capture.jpg':
                continue
                
            if filename.endswith((".jpg", ".png")):
                try:
                    employee_id = filename.split('.')[0]
                    image_path = os.path.join(faces_directory, filename)
                    print(f"Processing image: {image_path}")
                    
                    image = face_recognition.load_image_file(image_path)
                    print(f"Image loaded, shape: {image.shape}")
                    
                    encodings = face_recognition.face_encodings(image)
                    if len(encodings) > 0:
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_ids.append(employee_id)
                        print(f"Successfully encoded face for employee {employee_id}")
                    else:
                        print(f"No face found in {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        print(f"Finished loading faces. Total faces loaded: {len(self.known_face_encodings)}")

    def initialize_camera(self):
        """Initialize the camera"""
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Could not open camera")

    def capture_frame(self):
        """Capture a frame from the camera"""
        if self.camera is None:
            self.initialize_camera()
        ret, frame = self.camera.read()
        if not ret:
            raise Exception("Could not capture frame")
        return frame

    def identify_face(self, frame):
        """Identify a face in the given frame"""
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            print("\nStarting face identification...")
            print(f"Number of known faces: {len(self.known_face_encodings)}")
            
            # Find faces in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            if not face_locations:
                print("No face detected in frame")
                return None

            print(f"Found {len(face_locations)} faces in frame")
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            if not face_encodings:
                print("Could not encode face")
                return None

            print(f"Successfully encoded {len(face_encodings)} faces from frame")

            for face_encoding in face_encodings:
                # Compare with known faces
                if len(self.known_face_encodings) > 0:
                    # Calculer les distances faciales
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    print(f"Face distances: {face_distances}")
                    
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, 
                        face_encoding,
                        tolerance=0.7  # Augmenter la tolérance (défaut est 0.6)
                    )
                    
                    print(f"Matches results: {matches}")
                    
                    if True in matches:
                        first_match_index = matches.index(True)
                        matched_id = self.known_face_ids[first_match_index]
                        print(f"Match found! Employee ID: {matched_id}")
                        return matched_id
                    else:
                        print("No matches found with known faces")
                else:
                    print("No known faces to compare with")
            
            return None
        except Exception as e:
            print(f"Error in face identification: {e}")
            return None

    def release_camera(self):
        """Release the camera"""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
