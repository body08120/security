from views.main_view import MainView
from controllers.main_controller import MainController

def main():
    # Create the main view
    view = MainView()
    
    # Create the controller and connect it to the view
    controller = MainController(view)
    view.set_controller(controller)
    
    # Start the camera
    controller.start_camera()
    
    # Start the application
    view.mainloop()
    
    # Cleanup
    controller.cleanup()

if __name__ == "__main__":
    main()
