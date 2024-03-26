import os

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout, \
    QMessageBox, QHBoxLayout
from PyQt6.QtGui import QAction  # Corrected import for QAction
from umleditor.mvc_view.gui_view.class_card import ClassCard
from umleditor.mvc_view.gui_view.class_input_dialog import CustomInputDialog
from umleditor.mvc_controller.gui_controller import ControllerGUI


class GUIV2(QMainWindow):
    _process_task_signal = pyqtSignal(str, QWidget)

    def __init__(self):
        super().__init__()
        self.gridLayout = QGridLayout()
        self.centralWidget = QWidget(self)
        self.controller = ControllerGUI(self)  # Pass self reference to ControllerGUI
        self.setWindowTitle("UML Editor - GUI V2")
        self.setGeometry(300, 300, 850, 850)
        self.initUI()


    def get_signal(self):
        """
        Returns the signal used for processing tasks.
        """
        return self._process_task_signal

    def initUI(self):
        stylesheet_path = "src/umleditor/mvc_view/stylesheets/GuiV2Style.qss"
        print("Stylesheet exists:", os.path.exists(stylesheet_path))
        # Menu Actions
        actionAdd_Class = QAction('&Add Class', self)
        actionSave = QAction('&Save', self)
        actionLoad = QAction('&Load', self)
        actionExit = QAction('&Exit', self)
        actionHelp = QAction('&Help', self)

        # Connect actions
        actionAdd_Class.triggered.connect(self.on_add_class_clicked)
        actionSave.triggered.connect(lambda: self.controller.run('save', self))
        actionLoad.triggered.connect(lambda: self.controller.run('load', self))
        actionExit.triggered.connect(self.close)
        actionHelp.triggered.connect(self.help_click)

        # Setup menu bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(actionSave)
        fileMenu.addAction(actionLoad)
        fileMenu.addAction(actionExit)
        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction(actionAdd_Class)

        # Central widget and main layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        mainLayout = QHBoxLayout(self.centralWidget)

        # Sidebar
        sidebarWidget = QWidget()  # Sidebar container
        sidebarLayout = QVBoxLayout(sidebarWidget)
        sidebarWidget.setLayout(sidebarLayout)

        # Sidebar buttons
        btnFile = QPushButton("File")
        btnEdit = QPushButton("Edit")
        btnClasses = QPushButton("Classes")
        btnAttributes = QPushButton("Attributes")
        btnRelationships = QPushButton("Relationships")
        btnHelp = QPushButton("Help")

        # Add buttons to the sidebar layout
        sidebarLayout.addWidget(btnFile)
        sidebarLayout.addWidget(btnEdit)
        sidebarLayout.addWidget(btnClasses)
        sidebarLayout.addWidget(btnAttributes)
        sidebarLayout.addWidget(btnRelationships)
        sidebarLayout.addWidget(btnHelp)

        # Add sidebar to the main layout
        mainLayout.addWidget(sidebarWidget)
        sidebarWidget.setStyleSheet("background-color: red;")

        sidebarWidget.setObjectName("sidebarWidget")

        # Main content area
        contentWidget = QWidget()  # Container for the content area
        self.gridLayout = QGridLayout(contentWidget)  # Assign the grid layout to the content widget
        contentWidget.setLayout(self.gridLayout)

        # Add the content area to the main layout
        mainLayout.addWidget(contentWidget)

        # Set stretch factors
        mainLayout.setStretchFactor(sidebarWidget, 1)
        mainLayout.setStretchFactor(contentWidget, 4)

    def on_add_class_clicked(self):
        dialog = CustomInputDialog("Add Class", self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name = dialog.input_text.text()
            self.controller.run('class -a ' + class_name, None)

    def help_click(self):
        QMessageBox.information(self, "Help", "Helpful information goes here.")

    def add_class_card(self, class_name: str):
        # Ideally, you'll create and display a ClassCard widget
        print(f"Class {class_name} added")
        # Example: Adding a placeholder for the class card
        class_card = ClassCard(class_name)
        self.gridLayout.addWidget(class_card)


if __name__ == "__main__":
    app = QApplication([])

    with open("src/umleditor/mvc_view/stylesheets/GuiV2Style.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)
        print("Stylesheet content:", style[:100])

    gui = GUIV2()
    gui.show()
    app.exec()
