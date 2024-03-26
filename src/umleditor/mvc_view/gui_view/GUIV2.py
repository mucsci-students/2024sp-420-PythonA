
from PyQt6.QtWidgets import QMainWindow, QWidget, QWidget, QVBoxLayout, QAction,QMenuBar, QApplication
from class_card import ClassCard
from class_input_dialog import CustomInputDialog
from umleditor.mvc_controller.gui_controller import ControllerGUI

class GuiV2(QMainWindow):
    def __init__(self, controller: ControllerGUI):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle("UML Editor - GUI V2")
        self.setGeometry(300, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

