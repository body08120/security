import unittest  # Importation du module unittest pour les tests unitaires
from controllers.main_controller import DatabaseModel  # Importation de la classe DatabaseModel depuis le contrôleur

# Définition d'une classe de test pour le modèle de base de données
class TestDatabaseModel(unittest.TestCase):
    
    # Méthode de test pour vérifier l'équipement d'un employé
    def test_get_employee_equipment(self):
        model = DatabaseModel()  # Création d'une instance de DatabaseModel
        result = model.get_employee_equipment(1)  # Appel de la méthode avec un ID d'employé valide (1)
        
        # Définition de l'équipement attendu pour l'employé
        expected = [{'id_equipment': 1, 'equipment_name': 'Mousquetons', 'quantity_equipment': 14}]
        
        # Vérification que le résultat obtenu correspond à l'équipement attendu
        self.assertEqual(result, expected)

    # Méthode de test pour vérifier le comportement avec un ID d'employé invalide
    def test_get_employee_equipment_invalid_id(self):
        model = DatabaseModel()  # Création d'une instance de DatabaseModel
        result = model.get_employee_equipment(-1)  # Appel de la méthode avec un ID d'employé invalide (-1)
        
        # Définition de l'équipement attendu, qui devrait être vide pour un ID invalide
        expected = []  # Aucun équipement attendu
        
        # Vérification que le résultat obtenu correspond à l'équipement attendu (vide)
        self.assertEqual(result, expected)

# Point d'entrée principal pour exécuter les tests
if __name__ == '__main__':
    unittest.main()  # Exécution des tests