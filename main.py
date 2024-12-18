# Importation de la classe MainView depuis le module views.main_view
from views.main_view import MainView  
# Importation de la classe MainController depuis le module controllers.main_controller
from controllers.main_controller import MainController  

def main():
    # Création de la vue principale de l'application
    view = MainView()  
    
    # Création du contrôleur et connexion à la vue
    controller = MainController(view)  # Instanciation du contrôleur avec la vue
    view.set_controller(controller)  # Liaison du contrôleur à la vue
    
    # Démarrage de la caméra
    controller.start_camera()  # Appel de la méthode pour démarrer le flux vidéo de la caméra
    
    # Lancement de l'application
    view.mainloop()  # Démarrage de la boucle principale de l'interface graphique
    
    # Nettoyage des ressources
    controller.cleanup()  # Appel de la méthode pour libérer les ressources utilisées par le contrôleur

# Point d'entrée principal du programme
if __name__ == "__main__":
    main()  # Appel de la fonction main pour exécuter l'application