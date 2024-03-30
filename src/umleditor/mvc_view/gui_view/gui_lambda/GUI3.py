from PyQt6 import QtWidgets
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel)
from PyQt6.QtGui import QAction
from umleditor.mvc_view.gui_view.gui_cworld.class_card import ClassCard
from umleditor.mvc_view.gui_view.gui_cworld.class_input_dialog import CustomInputDialog


class GUI3(QMainWindow):
    _process_task_signal = pyqtSignal(str, QWidget)

    def __init__(self):
        super().__init__()
        self._size = 0
        self._maxsize = 10
        self.lstRelationships = QListWidget()
        self.gridLayout = QGridLayout()
        self.setWindowTitle("UML Editor - GUI V2.5")
        self.setGeometry(300, 300, 850, 850)
        self.initUI()
        self.applyDarkTheme()

    def get_signal(self):
        return self._process_task_signal

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.createActions()
        self.setupLayout()

    def createActions(self):
        self.actionAdd_Class = QAction('&Add Class', self)
        self.actionSave = QAction('&Save', self)
        self.actionLoad = QAction('&Load', self)
        self.actionExit = QAction('&Exit', self)
        self.actionHelp = QAction('&Help', self)

        self.actionAdd_Class.triggered.connect(self.on_add_class_clicked)
        self.actionSave.triggered.connect(self.help_click)
        self.actionLoad.triggered.connect(self.help_click)
        self.actionExit.triggered.connect(self.help_click)
        self.actionHelp.triggered.connect(self.help_click)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.actionSave)
        fileMenu.addAction(self.actionLoad)
        fileMenu.addAction(self.actionExit)
        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction(self.actionAdd_Class)


    def setupLayout(self):
        # Main layout for the entire window
        mainLayout = QHBoxLayout(self.centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)  # Removes margins so the page fills the window

        self.setupSidebar(mainLayout)

        contentWidget = QWidget()
        self.gridLayout = QGridLayout(contentWidget)
        contentWidget.setLayout(self.gridLayout)
        mainLayout.addWidget(contentWidget)
        mainLayout.setStretchFactor(contentWidget, 4)

    def setupSidebar(self, mainLayout):
        # Sidebar setup
        sidebarWidget = QWidget()
        sidebarWidget.setMaximumWidth(200)  # Maximum width of 200px
        sidebarLayout = QVBoxLayout(sidebarWidget)
        sidebarLayout.setContentsMargins(10, 10, 10, 10)  # Remove margins inside the sidebar

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

        mainLayout.setStretchFactor(sidebarWidget, 1)


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
        # Hover over a relationship to get the relationship type
        #

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

    def on_add_class_clicked(self):
        """
        Opens a dialog for adding a class and connects confirm button
        """
        self._dialog = CustomInputDialog(name="Add Class")
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
        class_card.get_enable_signal().connect(self.enable_widgets)

        # Increment the column; move to the next row if the current one is full.
        if self._column < self._max_column - 1:
            self._column += 1
        else:
            self._row += 1
            self._column = 0

        # Add the class card to the grid layout at the calculated row and column.
        self.gridLayout.addWidget(class_card, self._row, self._column)

    def help_click(self):
        QMessageBox.information(self, "Help", "Helpful information goes here.")

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
    from umleditor.mvc_controller.GUIV2_controller import ControllerGUI
    app = QtWidgets.QApplication([])
    gui = GUI3()
    controller = ControllerGUI(gui)  # Pass GUI instance to the controller
    gui.show()
    app.exec()
