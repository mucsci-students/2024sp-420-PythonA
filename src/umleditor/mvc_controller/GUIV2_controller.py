from umleditor.mvc_model.diagram import Diagram
from PyQt6 import QtWidgets
from umleditor.mvc_controller.controller import Controller

# This file began as a direct copy of gui_controller.py, Authored by Adam.

class ControllerGUI(Controller):
    """
    ControllerGui - Runs tasks signaled by GUIV2
        Run commands require updates to the gui e.g. methods found
        in run() 

    Parameters:
        window (GUIV2): The window instance of GUIV2.
    """

    def __init__(self, window) -> None:
        """
        Initializes Diagram, sets the view as a class variable,
        Connects signal that runs tasks

        Parameters:
            window (GUIV2): The window instance of GUIV2.
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
            # if isinstance(e, CE.FieldNotFoundError) or isinstance(e, CE.RelationDoesNotExistError):
            #    return
            self._window.invalid_input_message(str(e))
            return
        # Successful task
        if 'save' in task:
            self.save_file(widget)
            return
        if 'load' in task:
            self.load_file(widget)
            return
        if "class" in task:
            return
        if "mthd" in task:
            return
        if "field" in task:
            return
        if "prm" in task:
            return
        if "rel" in task:
            return
        else:
            self.acceptance_state(widget)

    def save_file(self, widget: QtWidgets):
        """
        Closes dialog and save file.

        Parameters:
            widget: ClassInputDialog.
        """

    def load_file(self, widget: QtWidgets):
        """
        Closes dialog and load file.

        Parameters:
            widget: ClassInputDialog.
        """
       
        self._window.delete_all_class_card()
        for entity in self._diagram._entities:
            class_card = self._window.add_class_card(entity._name)
            for field in entity._fields:
                class_card.add_field(field)
            for method in entity._methods:
                s = method.get_method_name()
                for param in method._params:
                    s += ' ' + param
                class_card.add_method(s)
            for relation in self._diagram._relations:
                if relation._source == entity:
                    s = relation._destination._name + ' ' + relation._type
                    class_card.add_relation(s)

        

    def acceptance_state(self, widget):
        """
        Makes text read-only and returns diagram to original state

        Parameters:
            widget: The widget instance.
        """
        widget.get_selected_line().setReadOnly(True)
        widget.get_selected_line().setStyleSheet("background-color: white;")
        widget.enable_context_menus(True)
        widget.deselect_line()
        self._window.enable_widgets(True, self)
