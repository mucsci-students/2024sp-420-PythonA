import sys, os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox, QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from umleditor.mvc_view.gui_view.class_input_dialog import ClassInputDialog
from umleditor.mvc_view.gui_view.class_card import ClassCard

class ViewGUI(QtWidgets.QMainWindow):
    # Signal triggered for task processing
    _process_task_signal = pyqtSignal(str, QWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(os.path.dirname(__file__))
        self._ui = uic.loadUi(os.path.join(os.path.dirname(__file__),"uml.ui"), self)
        self.connect_menu()
        self._x = 0
    
    def get_signal(self):
        return self._process_task_signal
    
    def connect_menu(self):
        self._ui.actionAdd_Class.triggered.connect(self.add_class_click)

    def invalid_input_message(self, warning: str):
        QMessageBox.critical(self, "Error", warning)

    #############           Add Class Methods            ############
    def add_class_click(self):
        self._dialog = ClassInputDialog()
        self._dialog.ok_button.clicked.connect(self.confirm_class_clicked)
        self._dialog.exec()

    def confirm_class_clicked(self):
        task = 'class -a ' + self._dialog.input_text.text()
        # Emit signal to controller to handle task
        self._process_task_signal.emit(task, self._dialog)
    
    def add_class_card(self, name: str):
        self._class_card = ClassCard(name) 
        # Add the custom widget to the central widget of the main window
        self._ui.gridLayout.addWidget(self._class_card, self._x, self._x)
        self._x = self._x + 1