import unittest  # Importation du module unittest pour les tests unitaires
from controllers.main_controller import DatabaseModel  # Importation de la classe DatabaseModel depuis le contrôleur



# Définition d'une classe de test pour le modèle de base de données

class TestDatabaseModel(unittest.TestCase):

        

    # Méthode de test pour vérifier l'équipement d'un employé avec un ID valide

    def test_get_employee_equipment_complete(self):

        # Création d'une instance de DatabaseModel pour accéder aux méthodes de la base de données

        model = DatabaseModel()  

        

        # Définition d'un ID d'employé valide pour le test

        valid_id = 1  

        

        # Définition de l'équipement attendu pour l'employé avec l'ID valide

        expected = [{'id_equipment': 1, 'equipment_name': 'Mousquetons', 'quantity_equipment': 14}]

        

        # Appel de la méthode get_employee_equipment avec l'ID valide pour obtenir le résultat

        result = model.get_employee_equipment(valid_id)

        

        # Vérification que le résultat obtenu correspond à l'équipement attendu

        self.assertEqual(result, expected)



        # Test pour un ID d'employé invalide

        invalid_id = -1  # Définition d'un ID d'employé invalide pour le test

        

        # Appel de la méthode avec l'ID invalide pour obtenir le résultat

        result_invalid = model.get_employee_equipment(invalid_id)

        

        # Définition de l'équipement attendu, qui devrait être vide pour un ID invalide

        expected_invalid = []  

        

        # Vérification que le résultat obtenu correspond à l'équipement attendu (vide)

        self.assertEqual(result_invalid, expected_invalid)



        # Test pour un ID d'employé inexistant

        nonexistent_id = 999  # Supposons que cet ID n'existe pas dans la base de données

        

        # Appel de la méthode avec l'ID inexistant pour obtenir le résultat

        result_nonexistent = model.get_employee_equipment(nonexistent_id)

        

        # Définition de l'équipement attendu, qui devrait être vide pour un ID inexistant

        expected_nonexistent = []  

        

        # Vérification que le résultat obtenu correspond à l'équipement attendu (vide)

        self.assertEqual(result_nonexistent, expected_nonexistent)



# Point d'entrée principal pour exécuter les tests

if __name__ == '__main__':

    unittest.main()  # Exécution des tests