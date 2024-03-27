from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel, QFrame)
from PyQt6.QtGui import QAction
from umleditor.mvc_view.gui_view.gui_cworld.class_card import ClassCard
from umleditor.mvc_view.gui_view.gui_cworld.class_input_dialog import CustomInputDialog


class GUIV2(QMainWindow):
    _process_task_signal = pyqtSignal(str, QWidget)

    def __init__(self):
        super().__init__()
        self.lstRelationships = QListWidget()
        self.gridLayout = QGridLayout()
        self.setWindowTitle("UML Editor - GUI V2")
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

        dialog = QDialog(self)
        dialog.setWindowTitle("File Actions")
        layout = QVBoxLayout()
        dialog.setMinimumWidth(300)
        if "background-color: #2b2b2b" in self.styleSheet():  # If currently running Dark Mode
            dialog.setStyleSheet("""
            
            QPushButton {
                color: white;
                background-color: #2B2B2B;
                border: 4px solid #69C68A;
                padding: 6px;
                border-radius: 4px;
                        }
            QPushButton:hover {
                background-color: #444644;
                 }"""
                                 )
        else:  # if not dark mode
            dialog.setStyleSheet("")  # Light Mode

        btnOpen = QPushButton("Open File")
        btnOpen.clicked.connect(self.openFile)
        layout.addWidget(btnOpen)

        btnNew = QPushButton("New File")
        btnNew.clicked.connect(self.newFile)
        layout.addWidget(btnNew)

        btnSave = QPushButton("Save")
        btnSave.clicked.connect(self.saveFile)
        layout.addWidget(btnSave)

        btnSaveAs = QPushButton("Save As")
        btnSaveAs.clicked.connect(self.saveAsFile)
        layout.addWidget(btnSaveAs)

        btnRedraw = QPushButton("Redraw")
        btnRedraw.clicked.connect(self.redrawDiagram)
        layout.addWidget(btnRedraw)

        dialog.setLayout(layout)
        dialog.exec()

    ### FILE ACTION STUBS

    def openFile(self):
        print("Stub: Open a file")

    def newFile(self):
        print("Stub: Create a new file")

    def saveFile(self):
        print("Stub: Save the current file")

    def saveAsFile(self):
        print("Stub: Save the current file as...")

    def redrawDiagram(self):
        print("Stub: Redraw the entire diagram")

    def editAction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Actions")
        dialog.setMinimumWidth(300)  # Ensures the dialog has a minimum width of 300px
        dialog.setObjectName("editActionDialog")  # Set object name for CSS selection

        layout = QVBoxLayout()

        # Adjusting the style for the dialog, if necessary
        if "background-color: #2b2b2b" in self.styleSheet():  # If currently in Dark Mode
            dialog.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #2B2B2B;
                border: 4px solid #BB4CC3;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #444644;
            }""")
        else:  # If not in Dark Mode
            dialog.setStyleSheet("")  # Apply Light Mode styling or keep it default

        # Button for Undo
        btnUndo = QPushButton("Undo")
        btnUndo.clicked.connect(self.undoAction)
        layout.addWidget(btnUndo)

        # Button for Redo
        btnRedo = QPushButton("Redo")
        btnRedo.clicked.connect(self.redoAction)
        layout.addWidget(btnRedo)

        # Button for Clear
        btnClear = QPushButton("Clear")
        btnClear.clicked.connect(self.clearAction)
        layout.addWidget(btnClear)

        dialog.setLayout(layout)
        dialog.exec()

    ### EDIT ACTION STUBS

    def undoAction(self):
        print("Stub: Undo the last action")

    def redoAction(self):
        print("Stub: Redo the last undone action")

    def clearAction(self):
        print("Stub: Clear the current selection or diagram")

    def classesAction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Class Actions")
        dialog.setMinimumWidth(300)  # Ensures the dialog has a minimum width of 300px
        dialog.setObjectName("classActionDialog")  # Set object name for CSS selection

        layout = QVBoxLayout()

        # Adjusting the style for the dialog, if necessary
        if "background-color: #2b2b2b" in self.styleSheet():  # If currently in Dark Mode
            dialog.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #2B2B2B;
                border: 4px solid #CB5551;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #444644;
            }""")
        else:  # If not in Dark Mode
            dialog.setStyleSheet("")  # Apply Light Mode styling or keep it default

        # Button for New Class
        btnNewClass = QPushButton("New Class")
        btnNewClass.clicked.connect(self.newClassAction)
        layout.addWidget(btnNewClass)

        # Button for Delete Class
        btnDeleteClass = QPushButton("Delete Class")
        btnDeleteClass.clicked.connect(self.deleteClassAction)
        layout.addWidget(btnDeleteClass)

        # Button for Rename Class
        btnRenameClass = QPushButton("Rename Class")
        btnRenameClass.clicked.connect(self.renameClassAction)
        layout.addWidget(btnRenameClass)

        dialog.setLayout(layout)
        dialog.exec()

    ### CLASS ACTION STUBS

    def newClassAction(self):
        print("Stub: Create a new class")

    def deleteClassAction(self):
        print("Stub: Delete an existing class")

    def renameClassAction(self):
        print("Stub: Rename an existing class")

    def attributesAction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Attributes and Methods")
        dialog.setMinimumWidth(300)
        if "background-color: #2b2b2b" in self.styleSheet():  # If currently in Dark Mode
            dialog.setStyleSheet("""
                            QPushButton {
                                color: white;
                                background-color: #2B2B2B;
                                border: 4px solid #C78640;
                                padding: 6px;
                                border-radius: 4px;
                            }
                            QPushButton:hover {
                                background-color: #444644;
                            }""")
        else:  # If not in Dark Mode
            dialog.setStyleSheet("")

        layout = QVBoxLayout(dialog)

        # Section for Methods
        methodsLabel = QLabel("Methods")
        layout.addWidget(methodsLabel)

        btnAddMethod = QPushButton("Add Method")
        btnAddMethod.clicked.connect(self.addMethodAction)
        layout.addWidget(btnAddMethod)

        btnRemoveMethod = QPushButton("Remove Method")
        btnRemoveMethod.clicked.connect(self.removeMethodAction)
        layout.addWidget(btnRemoveMethod)

        btnRenameMethod = QPushButton("Rename Method")
        btnRenameMethod.clicked.connect(self.renameMethodAction)
        layout.addWidget(btnRenameMethod)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)

        # Section for Fields
        fieldsLabel = QLabel("Fields")
        layout.addWidget(fieldsLabel)

        btnAddField = QPushButton("Add Field")
        btnAddField.clicked.connect(self.addFieldAction)
        layout.addWidget(btnAddField)

        btnRemoveField = QPushButton("Remove Field")
        btnRemoveField.clicked.connect(self.removeFieldAction)
        layout.addWidget(btnRemoveField)

        btnRenameField = QPushButton("Rename Field")
        btnRenameField.clicked.connect(self.renameFieldAction)
        layout.addWidget(btnRenameField)

        dialog.setLayout(layout)
        dialog.exec()

    ### ATTRIBUTE ACTION STUBS

    def addMethodAction(self):
        print("Stub: Add a new method")

    def removeMethodAction(self):
        print("Stub: Remove an existing method")

    def renameMethodAction(self):
        print("Stub: Rename a selected method")

    def addFieldAction(self):
        print("Stub: Add a new field")

    def removeFieldAction(self):
        print("Stub: Remove an existing field")

    def renameFieldAction(self):
        print("Stub: Rename a selected field")

    def relationshipsAction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Relationships")
        dialog.setMinimumWidth(300)
        if "background-color: #2b2b2b" in self.styleSheet():  # If currently in Dark Mode
            dialog.setStyleSheet("""
                        QPushButton {
                            color: white;
                            background-color: #2B2B2B;
                            border: 4px solid #4882CF;
                            padding: 6px;
                            border-radius: 4px;
                        }
                        QPushButton:hover {
                            background-color: #444644;
                        }""")
        else:  # If not in Dark Mode
            dialog.setStyleSheet("")  # Apply Light Mode styling or keep it default

        layout = QVBoxLayout(dialog)

        # Section for Relationships
        relationshipsLabel = QLabel("Relationships")
        layout.addWidget(relationshipsLabel)

        btnCreateRelationship = QPushButton("Create Relationship")
        btnCreateRelationship.clicked.connect(self.createRelationshipAction)
        layout.addWidget(btnCreateRelationship)

        btnRemoveRelationship = QPushButton("Remove Relationship")
        btnRemoveRelationship.clicked.connect(self.removeRelationshipAction)
        layout.addWidget(btnRemoveRelationship)

        dialog.exec()

    # Placeholder methods for actions
    def createRelationshipAction(self):
        print("Create Relationship action")

    def removeRelationshipAction(self):
        print("Remove Relationship action")

    def helpAction(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")
        dialog.setMinimumWidth(300)

        if "background-color: #2b2b2b" in self.styleSheet():  # If currently in Dark Mode
            dialog.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: #2B2B2B;
                    border: 2px solid #BB4A83;
                    padding: 6px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #444644;
                }
                QVBoxLayout {
                    background-color: #2b2b2b;
                }
            """)
        else:  # If not in Dark Mode
            # Apply Light Mode styling or keep it default
            dialog.setStyleSheet("""
                QPushButton {
                    background-color: #ECECEC;
                    border: 2px solid #BB4A83;
                    padding: 6px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #DCDCDC;
                }
                QVBoxLayout {
                    background-color: white;
                }
            """)

        layout = QVBoxLayout(dialog)

        # Button for Loading README
        btnLoadReadme = QPushButton("Load README")
        btnLoadReadme.clicked.connect(self.loadReadmeAction)
        layout.addWidget(btnLoadReadme)

        # Button for Help on Classes
        btnHelpClasses = QPushButton("Help on Classes")
        btnHelpClasses.clicked.connect(self.helpClassesAction)
        layout.addWidget(btnHelpClasses)

        # Button for Help on Relationships
        btnHelpRelationships = QPushButton("Help on Relationships")
        btnHelpRelationships.clicked.connect(self.helpRelationshipsAction)
        layout.addWidget(btnHelpRelationships)

        # Button for Help on Attributes
        btnHelpAttributes = QPushButton("Help on Attributes")
        btnHelpAttributes.clicked.connect(self.helpAttributesAction)
        layout.addWidget(btnHelpAttributes)

        dialog.exec()
    ###STUBS FOR HELP
    def loadReadmeAction(self):
        print("Load README action")

    def helpClassesAction(self):
        print("Help on Classes action")

    def helpRelationshipsAction(self):
        print("Help on Relationships action")

    def helpAttributesAction(self):
        print("Help on Attributes action")

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
            # Emit the signal to the controller with the appropriate task and widget
            self._process_task_signal.emit('class -a ' + class_name, self)

    def help_click(self):
        QMessageBox.information(self, "Help", "Helpful information goes here.")

    ###THEMES###
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

    gui = GUIV2()
    gui.show()
    app.exec()
