import os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QWidget, QMenuBar, QGridLayout
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
        self._ui = uic.loadUi(os.path.join(os.path.dirname(__file__),"uml.ui"), self)
        self.connect_menu()
        # Create grid and max sizes
        self._grid_layout = QGridLayout(self._ui.centralwidget)
        self._max_size = 20
        self._max_column = 5
        self._size = 0
        self._row = 0
        self._column = 0
    
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
        if self._size >= self._max_size:
            self.invalid_input_message("No more than " + str(self._max_size) + " Class Cards in a single diagram!")
            return
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
        class_card.get_enable_signal().connect(self.enable_widgets)
        if self._size == 0:
            self._grid_layout.addWidget(class_card, self._row, self._column)
            self._size += 1
        else: 
            if self._column < self._max_column - 1:
                self._column += 1
            else:
                self._row += 1
                self._column = 0
            self._size += 1
            self._grid_layout.addWidget(class_card, self._row, self._column)

    def delete_class_card(self, name: str):
        """
        Removes the ClassCard widget for the specified class from the layout.
        """
        for i in range(self._grid_layout.count()): 
            item = self._grid_layout.itemAt(i)
            if item is not None:
                class_card = item.widget()
                if isinstance(class_card, ClassCard) and class_card._name == name:
                    self._grid_layout.removeWidget(class_card)
                    class_card.deleteLater() 
                    self._size -= 1  # Decrement the total count of class cards

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

