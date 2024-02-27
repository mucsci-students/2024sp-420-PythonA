from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
from umleditor.mvc_model.diagram import Diagram
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QInputDialog, QLineEdit
from PyQt6.QtCore import QDir
from umleditor.mvc_controller.controller import Controller
from umleditor.mvc_view.gui_view.class_input_dialog import ClassInputDialog
from umleditor.mvc_model.custom_exceptions import CustomExceptions as CE

class ControllerGUI (Controller):
    """
    ControllerGui - Runs tasks signaled by ViewGui
        Run commands require updates to the gui e.g. methods found
        in run() 

    Parameters:
        window (ViewGUI): The window instance of ViewGUI.
    """

    def __init__(self, window: ViewGUI) -> None:
        """
        Initializes Diagram, sets the view as a class variable,
        Connects signal that runs tasks

        Parameters:
            window (ViewGUI): The window instance of ViewGUI.
        """
        super().__init__()
        self._window = window
        self._diagram = Diagram()
        self._window.get_signal().connect(self.run)

    def run(self, task: str, widget: QtWidgets):
        """
        Runs the specified task.

        Parameters:
            task (str): The task to run.
            widget (QtWidgets): Used to set particular widget to its completed state
        """
        print(task)
        try:
            out = super().run(task)
        except Exception as e:
            # Ignore attempting to delete things that don't exist
            if isinstance(e, CE.FieldNotFoundError):
                pass
            self._window.invalid_input_message(str(e))
            return
        # Successful task
        if "class -a" in task:
            self.add_class(task, widget)
        elif "fld" in task:
            self.add_field(widget)
    
    def add_class(self, task: str, widget: QtWidgets):
        """
        Closes dialog and creates class card.

        Parameters:
            task (str): Used for class name.
            widget: ClassInputDialog.
        """
        widget.reject()
        entity_name = task.split()[-1]
        self._window.add_class_card(entity_name)
    
    def add_field(self, widget):
        """
        Makes text read-only and returns diagram to original state

        Parameters:
            widget: The widget instance.
        """
        print("Add Field Called")
        print(widget.get_selected_line().text())
        widget.get_selected_line().setReadOnly(True)
        widget.get_selected_line().setStyleSheet("background-color: white;")
        widget.enable_context_menus(True)
        self._window.enable_widgets(True, self)
        
