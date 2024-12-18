# Importation des bibliothèques nécessaires pour la connexion à la base de données MySQL et la gestion des données
import mysql.connector  # Importation de la bibliothèque pour se connecter à MySQL
from mysql.connector import Error  # Importation des erreurs spécifiques à MySQL

# Définition de la classe DatabaseModel pour interagir avec la base de données
class DatabaseModel:
    def __init__(self):
        # Initialisation de la connexion à la base de données
        try:
            self.connection = mysql.connector.connect(
                host='localhost',  # Adresse du serveur MySQL
                database='security_db',  # Nom de la base de données
                user='root',  # Nom d'utilisateur pour la connexion
                password=''  # Mot de passe pour la connexion
            )
            if self.connection.is_connected():  # Vérifier si la connexion est établie
                print("Connected to MySQL database")  # Afficher un message de succès
        except Error as e:  # Gérer les erreurs de connexion
            print(f"Error: {e}")  # Afficher le message d'erreur

    def verify_employee(self, employee_id):
        """Vérifier si un employé existe et obtenir ses détails"""
        try:
            cursor = self.connection.cursor(dictionary=True)  # Créer un curseur pour exécuter des requêtes
            query = "SELECT * FROM employee WHERE id_employee = %s"  # Requête pour vérifier l'employé
            print(f"Verifying employee with ID: {employee_id}")  # Afficher l'ID de l'employé vérifié
            cursor.execute(query, (employee_id,))  # Exécuter la requête avec l'ID de l'employé
            result = cursor.fetchone()  # Récupérer le résultat de la requête
            print(f"Database result: {result}")  # Afficher le résultat de la base de données
            cursor.close()  # Fermer le curseur
            return result  # Retourner le résultat
        except Error as e:  # Gérer les erreurs lors de la vérification
            print(f"Database error during verification: {e}")  # Afficher le message d'erreur
            return None  # Retourner None en cas d'erreur

    def get_employee_equipment(self, employee_id):
        """Obtenir l'équipement assigné à un employé"""
        try:
            cursor = self.connection.cursor(dictionary=True)  # Créer un curseur pour exécuter des requêtes
            query = ("SELECT e.* FROM equipment e "
                     "JOIN have h ON e.id_equipment = h.id_equipment "
                     "WHERE h.id_employee = %s")  # Requête pour obtenir l'équipement de l'employé
            cursor.execute(query, (employee_id,))  # Exécuter la requête avec l'ID de l'employé
            result = cursor.fetchall()  # Récupérer tous les résultats
            cursor.close()  # Fermer le curseur
            return result  # Retourner les résultats
        except Error as e:  # Gérer les erreurs lors de la récupération de l'équipement
            print(f"Error: {e}")  # Afficher le message d'erreur
            return []  # Retourner une liste vide en cas d'erreur

    def assign_equipment(self, employee_id, equipment_id):
        """Assigner un équipement à un employé et diminuer la quantité"""
        try:
            cursor = self.connection.cursor()  # Créer un curseur pour exécuter des requêtes
            
            # Vérifier la quantité disponible
            cursor.execute(
                "SELECT quantity_equipment FROM equipment WHERE id_equipment = %s",  # Requête pour vérifier la quantité
                (equipment_id,)  # ID de l'équipement à vérifier
            )
            result = cursor.fetchone()  # Récupérer le résultat de la requête
            if not result or result[0] <= 0:  # Vérifier si l'équipement est disponible
                print(f"Equipment {equipment_id} not available (quantity: {result[0] if result else 0})")  # Afficher un message d'indisponibilité
                return False  # Retourner False si l'équipement n'est pas disponible
            
            # Diminuer la quantité
            cursor.execute(
                "UPDATE equipment SET quantity_equipment = quantity_equipment - 1 WHERE id_equipment = %s",  # Requête pour diminuer la quantité
                (equipment_id,)  # ID de l'équipement à mettre à jour
            )
            
            # Ajouter la relation
            cursor.execute(
                "INSERT INTO have (id_employee, id_equipment) VALUES (%s, %s)",  # Requête pour ajouter l'équipement à l'employé
                (employee_id, equipment_id)  # ID de l'employé et de l'équipement
            )
            
            self.connection.commit()  # Valider les changements dans la base de données
            print(f"Equipment {equipment_id} assigned to employee {employee_id}")  # Afficher un message de succès
            return True  # Retourner True en cas de succès
            
        except Exception as e:  # Gérer les exceptions lors de l'assignation
            print(f"Error assigning equipment: {e}")  # Afficher le message d'erreur
            self.connection.rollback()  # Annuler les changements en cas d'erreur
            return False  # Retourner False en cas d'erreur

    def unassign_equipment(self, employee_id, equipment_id):
        """Désassigner un équipement d'un employé et augmenter la quantité"""
        try:
            cursor = self.connection.cursor()  # Créer un curseur pour exécuter des requêtes
            
            # Supprimer la relation
            cursor.execute(
                "DELETE FROM have WHERE id_employee = %s AND id_equipment = %s",  # Requête pour supprimer la relation
                (employee_id, equipment_id)  # ID de l'employé et de l'équipement
            )
            
            # Augmenter la quantité
            cursor.execute(
                "UPDATE equipment SET quantity_equipment = quantity_equipment + 1 WHERE id_equipment = %s",  # Requête pour augmenter la quantité
                (equipment_id,)  # ID de l'équipement à mettre à jour
            )
            
            self.connection.commit()  # Valider les changements dans la base de données
            print(f"Equipment {equipment_id} unassigned from employee {employee_id}")  # Afficher un message de succès
            return True  # Retourner True en cas de succès
            
        except Exception as e:  # Gérer les exceptions lors de la désassignation
            print(f"Error unassigning equipment: {e}")  # Afficher le message d'erreur
            self.connection.rollback()  # Annuler les changements en cas d'erreur
            return False  # Retourner False en cas d'erreur

    def get_all_equipment(self):
        """Obtenir tous les équipements"""
        try:
            cursor = self.connection.cursor(dictionary=True)  # Créer un curseur pour exécuter des requêtes
            query = "SELECT * FROM equipment"  # Requête pour obtenir tous les équipements
            cursor.execute(query)  # Exécuter la requête
            result = cursor.fetchall()  # Récupérer tous les résultats
            cursor.close()  # Fermer le curseur
            return result  # Retourner les résultats
        except Error as e:  # Gérer les erreurs lors de la récupération des équipements
            print(f"Error: {e}")  # Afficher le message d'erreur
            return []  # Retourner une liste vide en cas d'erreur

    def get_all_employees(self):
        """Obtenir tous les employés avec leurs photos"""
        try:
            cursor = self.connection.cursor(dictionary=True)  # Créer un curseur pour exécuter des requêtes
            query = "SELECT * FROM employee"  # Requête pour obtenir tous les employés
            cursor.execute(query)  # Exécuter la requête
            result = cursor.fetchall()  # Récupérer tous les résultats
            cursor.close()  # Fermer le curseur
            return result  # Retourner les résultats
        except Error as e:  # Gérer les erreurs lors de la récupération des employés
            print(f"Error getting employees: {e}")  # Afficher le message d'erreur
            return []  # Retourner une liste vide en cas d'erreur

    def __del__(self):
        """Destructeur pour fermer la connexion à la base de données"""
        if hasattr(self, 'connection') and self.connection.is_connected():  # Vérifier si la connexion existe et est active
            self.connection.close()  # Fermer la connexion à la base de données
            print("Database connection closed.")  # Afficher un message de confirmation
