from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QInputDialog, QLineEdit
from PyQt6.QtCore import QDir


class ControllerGUI:
    
    def __init__(self, window: ViewGUI) -> None:
        self._window = window
        # Used for detecting when tasks need run
        self._window.get_signal().connect(self.run)

    def run(self, task: str):
        if "class -a" in task:
            self.run_add_class(task)
        # Parse / Run Command
        # If success, return true
        # Else, create error messagebox and return false
    
    def run_add_class(self, task):
        #TODO Parse
        success = True
        warning = "Invalid class name!" 
        print(task)
        if success:
            self._window.close_class_dialog()
            self._window.add_class_card()
        else:
            self._window.invalid_input_message(warning)
        
