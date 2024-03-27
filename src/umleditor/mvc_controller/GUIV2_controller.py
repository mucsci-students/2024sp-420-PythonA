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
        if 'class -r' in task:
            self.rename_class(task, widget)
            return
        if "class -a" in task:
            self.add_class(task, widget)
        # No action required after deleting
        elif "-d" in task:
            self.delete_class(task, widget)
        else:
            self.acceptance_state(widget)

    def save_file(self, widget: QtWidgets):
        """
        Closes dialog and save file.

        Parameters:
            widget: ClassInputDialog.
        """
        widget.reject()

    def load_file(self, widget: QtWidgets):
        """
        Closes dialog and load file.

        Parameters:
            widget: ClassInputDialog.
        """
        widget.reject()
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

    def rename_class(self, task: str, widget: QtWidgets):
        words = task.split()
        widget.accept_new_name(words[-1])

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

    def delete_class(self, task: str, widget: QtWidgets):
        """
        Deletes class card.

        Parameters:
            widget: The widget instance.
        """
        class_name = task.split()[-1]
        self._window.delete_class_card(class_name)

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
