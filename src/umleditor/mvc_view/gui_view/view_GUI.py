import os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QMenuBar, QLineEdit
from PyQt6.QtCore import pyqtSignal
from umleditor.mvc_view.gui_view.class_input_dialog import ClassInputDialog
from umleditor.mvc_view.gui_view.class_card import ClassCard

class ViewGUI(QtWidgets.QMainWindow):
    """
    ViewGUI - Main application window for the UML diagram editor.

    Signals:
        _process_task_signal (str, QWidget): Signal triggered for task processing.
    """
    _process_task_signal = pyqtSignal(str, QWidget)

    def __init__(self, *args, **kwargs):
        """
        Initializes the ViewGUI instance and connect menu buttons
        """
        super().__init__(*args, **kwargs)
        print(os.path.dirname(__file__))
        self._ui = uic.loadUi(os.path.join(os.path.dirname(__file__),"uml.ui"), self)
        self.connect_menu()
        self._x = 0
    
    def get_signal(self):
        """
        Gets the process task signal.

        Returns:
            pyqtSignal: The process task signal.
        """
        return self._process_task_signal
    
    def connect_menu(self):
        """
        Connects menu actions to corresponding methods.
        """
        self._ui.actionAdd_Class.triggered.connect(self.add_class_click)

    def invalid_input_message(self, warning: str):
        """
        Displays an error message dialog.

        Args:
            warning (str): The warning message.
        """
        QMessageBox.critical(self, "Error", warning)
    
    def forward_signal(self, task: str, widget: QWidget):
        """
        Forwards a signal to process a task.

        Args:
            task (str): The task to process.
            widget (QWidget): The widget associated with the task.
        """
        self._process_task_signal.emit(task, widget)

    #############           Add Class Methods            ############
    def add_class_click(self):
        """
        Opens a dialog for adding a class and connects confirm button
        """
        self._dialog = ClassInputDialog()
        self._dialog.ok_button.clicked.connect(self.confirm_class_clicked)
        self._dialog.exec()

    def confirm_class_clicked(self):
        """
        On Confirm emits signal to process task
        """
        task = 'class -a ' + self._dialog.input_text.text()
        # Emit signal to controller to handle task
        self._process_task_signal.emit(task, self._dialog)
    
    def add_class_card(self, name: str):
        """
        Adds a class card widget to the main window.
        Connects signals for sending tasks and disabling other widgets

        Args:
            name (str): The name of the class.
        """
        class_card = ClassCard(name) 
        class_card.get_task_signal().connect(self.forward_signal)
        class_card.get_disable_signal().connect(self.enable_widgets)
        self._ui.gridLayout.addWidget(class_card, self._x, self._x)
        self._x = self._x + 1

    def enable_widgets(self, enabled: bool, active_widget: QWidget):
        """
        Toggles unselected Widgets. False = Disabled, True = Enabled

        Args:
            enabled (bool): Flag indicating whether widgets should be enabled.
            active_widget (QWidget): The active ClassCard widget.
        """
        for child_widget in self.findChildren(QWidget):
            if isinstance(child_widget, ClassCard) or isinstance(child_widget, QMenuBar):
                if enabled or child_widget is active_widget:
                    child_widget.setEnabled(True)
                else:
                    child_widget.setEnabled(False)
        active_widget.disable_unselected_items()

