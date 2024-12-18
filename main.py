"""Point d'entrée principal de l'application."""
from views.main_view import MainView
from controllers.main_controller import MainController


def main():
    """Fonction principale qui démarre l'application."""
    # Création de la vue principale
    view = MainView()
    
    # Création du contrôleur et connexion à la vue
    controller = MainController(view)
    view.set_controller(controller)
    
    # Démarrage de la caméra
    controller.start_camera()
    
    # Lancement de l'application
    view.mainloop()
    
    # Nettoyage des ressources
    controller.cleanup()


if __name__ == "__main__":
    main()