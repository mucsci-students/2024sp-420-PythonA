from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
from umleditor.mvc_model.diagram import Diagram
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QInputDialog, QLineEdit
from PyQt6.QtCore import QDir
from umleditor.mvc_controller.controller import Controller

class ControllerGUI (Controller):
    
    def __init__(self, window: ViewGUI) -> None:
        super().__init__()
        self._window = window
        self._diagram = Diagram()
        # Used for detecting when tasks need run
        self._window.get_signal().connect(self.run)

    def run(self, task: str):
        try:
            out = super().run(task)
        except Exception as e:
            self._window.invalid_input_message(str(e))
            return
        # Successful task
        if "class -a" in task:
            self.add_class(task)

        # Parse / Run Command
        # If success, return true
        # Else, create error messagebox and return false
    
    def add_class(self, task):
        entity_name = task.split()[-1]
        self._window.close_class_dialog()
        self._window.add_class_card(entity_name)
        
