import os
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel)
from PyQt6.QtGui import QAction
from umleditor.mvc_view.gui_view.class_card import ClassCard
from umleditor.mvc_view.gui_view.class_input_dialog import CustomInputDialog
from umleditor.mvc_controller.gui_controller import ControllerGUI


class GUIV2(QMainWindow):
    _process_task_signal = pyqtSignal(str, QWidget)

    def __init__(self):
        super().__init__()
        self.lstRelationships = QListWidget()
        self.gridLayout = QGridLayout()
        self.centralWidget = QWidget(self)
        self.controller = ControllerGUI(self)
        self.setWindowTitle("UML Editor - GUI V2")
        self.setGeometry(300, 300, 850, 850)
        self.initUI()
        self.applyDarkTheme()

    def get_signal(self):
        return self._process_task_signal

    def initUI(self):
        actionAdd_Class = QAction('&Add Class', self)
        actionSave = QAction('&Save', self)
        actionLoad = QAction('&Load', self)
        actionExit = QAction('&Exit', self)
        actionHelp = QAction('&Help', self)

        actionAdd_Class.triggered.connect(self.on_add_class_clicked)
        actionSave.triggered.connect(lambda: self.controller.run('save', self))
        actionLoad.triggered.connect(lambda: self.controller.run('load', self))
        actionExit.triggered.connect(self.close)
        actionHelp.triggered.connect(self.help_click)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(actionSave)
        fileMenu.addAction(actionLoad)
        fileMenu.addAction(actionExit)
        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction(actionAdd_Class)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        mainLayout = QHBoxLayout(self.centralWidget)

        sidebarWidget = QWidget()
        sidebarLayout = QVBoxLayout(sidebarWidget)
        sidebarWidget.setLayout(sidebarLayout)

        # Define button info with actions
        buttons_info = [
            ("File", "#69C68A", self.fileAction),
            ("Edit", "#BB4CC3", self.editAction),
            ("Classes", "#CB5551", self.classesAction),
            ("Attributes", "#C78640", self.attributesAction),
            ("Relationships", "#4882CF", self.relationshipsAction),
            ("Help", "#BB4A83", self.helpAction),
            ("Themes", "#93C756", self.showThemeDialog)
        ]

        for text, color, action in buttons_info:
            btn = QPushButton(text)
            btn.setStyleSheet(f"QPushButton {{border: 2px solid {color};}}")
            btn.clicked.connect(action)
            sidebarLayout.addWidget(btn)

        lblRelationships = QLabel("Relationships")
        lblRelationships.setObjectName("lblRelationships")
        sidebarLayout.addWidget(lblRelationships)

        self.lstRelationships = QListWidget()
        self.lstRelationships.setObjectName("lstRelationships")
        sidebarLayout.addWidget(self.lstRelationships)

        # Example items (for demonstration purposes)
        self.lstRelationships.addItem("Class1 -> Class2")
        self.lstRelationships.addItem("Class3 -> Class4")

        mainLayout.addWidget(sidebarWidget)
        sidebarWidget.setObjectName("sidebarWidget")

        contentWidget = QWidget()
        self.gridLayout = QGridLayout(contentWidget)
        contentWidget.setLayout(self.gridLayout)
        mainLayout.addWidget(contentWidget)

        mainLayout.setStretchFactor(sidebarWidget, 1)
        mainLayout.setStretchFactor(contentWidget, 4)

    def fileAction(self):
        print("File action triggered")

    def editAction(self):
        print("Edit action triggered")

    def classesAction(self):
        print("Classes action triggered")

    def attributesAction(self):
        print("Attributes action triggered")

    def relationshipsAction(self):
        print("Relationships action triggered")

    def helpAction(self):
        print("Help action triggered")

    def showThemeDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Theme")

        # Layout for radio buttons
        layout = QVBoxLayout()

        # Radio buttons for theme selection
        self.radio_dark_theme = QRadioButton("Dark Theme")
        self.radio_light_theme = QRadioButton("Light Theme")

        # Set the default theme selection based on the current stylesheet
        if "background-color: #2b2b2b" in self.styleSheet():
            self.radio_dark_theme.setChecked(True)
        else:
            self.radio_light_theme.setChecked(True)

        layout.addWidget(self.radio_dark_theme)
        layout.addWidget(self.radio_light_theme)

        # Dialog button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        dialog.setLayout(layout)

        # If the user clicks OK, apply the selected theme
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.radio_dark_theme.isChecked():
                self.applyDarkTheme()
            elif self.radio_light_theme.isChecked():
                self.applyLightTheme()

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

    def applyDarkTheme(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
            color: white;
        }
        QPushButton {
            color: white;
            background-color: #2B2B2B;
            border: 4px solid #050505;
            padding: 6px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #444644;
        }
        #sidebarWidget {
            background-color: #212121;
            max-width: 200px;
            }
        #lstRelationships {
            background-color: #2B2B2B;
            color: white;
            border: 2px solid #050505;
            padding: 6px;
            border-radius: 4px
            }
        #lblRelationships {
            color: white;
            }
        """)
        self.findChild(QLabel, "lblRelationships").setAlignment(Qt.AlignmentFlag.AlignHCenter)

    def applyLightTheme(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: white;
            color: black;
        }
        QPushButton {
            background-color: #C9C9C9;
            border: 2px solid #050505;
            padding: 6px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #595A59;
        }
        #sidebarWidget {
            background-color: #9C9C9C;
            max-width: 200px;
            }
        #lstRelationships {
            background-color: white;
            color: black;
            border: 2px solid white;
            padding: 6px;
            border-radius: 4px
            }
        #lblRelationships {
            color: white;
            }
        """)
        self.findChild(QLabel, "lblRelationships").setAlignment(Qt.AlignmentFlag.AlignHCenter)


if __name__ == "__main__":
    app = QApplication([])

    stylesheet_path = "../stylesheets/GuiV2Style.qss"
    with open(stylesheet_path, "r") as f:
        style = f.read()
        app.setStyleSheet(style)
        print("Stylesheet content:", style[:100])

    gui = GUIV2()
    gui.show()
    app.exec()
