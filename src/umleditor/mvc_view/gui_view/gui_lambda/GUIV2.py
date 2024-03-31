from umleditor.mvc_model.diagram import Diagram
from PyQt6.QtCore import pyqtSignal, Qt, QPoint
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel, QFrame,
                             QFileDialog)
from PyQt6.QtGui import QAction
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.newClassDialog import NewClassDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.deleteClassDialog import DeleteClassDialog
from umleditor.mvc_view.gui_view.gui_lambda.GUIV2_class_card import ClassCard
from umleditor.mvc_view.gui_view.gui_cworld.class_input_dialog import CustomInputDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.addMethodDialog import AddMethodDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.changeParams import ChangeParamsDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.createRelationshipDialog import CreateRelationshipDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.deleteMethodDialog import RemoveMethodDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.deleteRelationshipDialog import RemoveRelationshipDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.fieldDialogs import AddFieldDialog, RenameFieldDialog, \
    RemoveFieldDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.renameClassDialog import RenameClassDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.renameMethodDialog import RenameMethodDialog


class GUIV2(QMainWindow):
    _process_task_signal = pyqtSignal(str, QWidget)

    def __init__(self):
        super().__init__()
        self._diagram = Diagram()
        self.lstRelationships = QListWidget()
        self.gridLayout = QGridLayout()
        self.setWindowTitle("UML Editor - GUI V2")
        self.setGeometry(300, 300, 850, 850)
        self.initUI()
        self.applyDarkTheme()
        self.currentFilePath = " "
        self.fields = ["field1", "field2", "field3"]

    def get_signal(self):
        return self._process_task_signal

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.createActions()
        self.setupLayout()

    def createActions(self):
        # Adding Classes
        self.actionAdd_Class = QAction('&Add Class', self)
        self.actionAdd_Class.triggered.connect(self.newClassAction)

        # Deleting Classes
        self.actionDelete_Class = QAction('&Delete Class', self)
        self.actionDelete_Class.triggered.connect(self.deleteClassAction)

        # Renaming Classes
        self.actionRename_Class = QAction('&Rename Class', self)
        self.actionRename_Class.triggered.connect(self.renameClassAction)

        # Saving and Loading
        self.actionSave = QAction('&Save', self)
        self.actionSave.triggered.connect(self.saveFile)

        # self.actionSaveAs = QAction('Save &As...', self)
        # self.actionSaveAs.triggered.connect(self.saveAsFile)

        self.actionLoad = QAction('&Load', self)
        self.actionLoad.triggered.connect(self.openFile)

        self.actionExit = QAction('&Exit', self)
        self.actionExit.triggered.connect(self.close)  # 'close' is a built-in method to close the window

        self.actionHelp = QAction('&Help', self)
        self.actionHelp.triggered.connect(self.help_click)

        self.actionChangeMethodParams = QAction('&Parameters', self)
        self.actionChangeMethodParams.triggered.connect(self.changeMethodParamsAction)

        # Managing Relationships
        self.actionAdd_Relationship = QAction('Add &Relationship', self)
        self.actionAdd_Relationship.triggered.connect(self.createRelationshipAction)

        self.actionRemove_Relationship = QAction('Remove &Relationship', self)
        self.actionRemove_Relationship.triggered.connect(self.removeRelationshipAction)

        # Managing Fields
        self.actionAdd_Field = QAction('Add &Field', self)
        self.actionAdd_Field.triggered.connect(self.addFieldAction)

        self.actionRemove_Field = QAction('Remove &Field', self)
        self.actionRemove_Field.triggered.connect(self.removeFieldAction)

        self.actionRename_Field = QAction('Rename &Field', self)
        self.actionRename_Field.triggered.connect(self.renameFieldAction)

        # Managing Methods
        self.actionAdd_Method = QAction('Add &Method', self)
        self.actionAdd_Method.triggered.connect(self.addMethodAction)

        self.actionRemove_Method = QAction('Remove &Method', self)
        self.actionRemove_Method.triggered.connect(self.removeMethodAction)

        self.actionRename_Method = QAction('Rename &Method', self)
        self.actionRename_Method.triggered.connect(self.renameMethodAction)

        # Adding actions to the menu
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(self.actionSave)
        # fileMenu.addAction(self.actionSaveAs)
        fileMenu.addAction(self.actionLoad)
        fileMenu.addAction(self.actionExit)

        editMenu = menuBar.addMenu('&Edit')
        editMenu.addAction(self.actionAdd_Class)
        editMenu.addAction(self.actionDelete_Class)
        editMenu.addAction(self.actionRename_Class)
        editMenu.addSeparator()  # Adds a visual separator between menu items
        editMenu.addAction(self.actionAdd_Relationship)
        editMenu.addAction(self.actionRemove_Relationship)
        editMenu.addSeparator()
        editMenu.addAction(self.actionAdd_Field)
        editMenu.addAction(self.actionRemove_Field)
        editMenu.addAction(self.actionRename_Field)
        editMenu.addSeparator()
        editMenu.addAction(self.actionAdd_Method)
        editMenu.addAction(self.actionRemove_Method)
        editMenu.addAction(self.actionRename_Method)

        helpMenu = menuBar.addMenu('&Help')
        helpMenu.addAction(self.actionHelp)

    def setupLayout(self):
        # Main layout for the entire window
        mainLayout = QHBoxLayout(self.centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)  # Removes margins so the page fills the window

        # Setup sidebar part of the layout
        self.setupSidebar(mainLayout)

        # Initialize DiagramArea and add it directly to the mainLayout
        self.diagramArea = DiagramArea()
        mainLayout.addWidget(self.diagramArea)
        mainLayout.setStretchFactor(self.diagramArea, 4)  # Give the diagram area more space compared to the sidebar


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

        # # Example items (for demonstration purposes)
        # self.lstRelationships.addItem("Class1 -> Class2")
        # self.lstRelationships.addItem("Class3 -> Class4")

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

        # btnRedraw = QPushButton("Redraw")
        # btnRedraw.clicked.connect(self.redrawDiagram)
        # layout.addWidget(btnRedraw)

        dialog.setLayout(layout)
        dialog.exec()

    ### FILE ACTION STUBS

    def openFile(self):
        self._process_task_signal.emit('load')
        
    def newFile(self):
        # Logic to reset the application state for a new file
        print("Creating a new file...")
        # Example: Clearing the UI, resetting data models, etc.

    def saveFile(self):
        # Assuming self.currentFilePath holds the path of the current file
        self._process_task_signal.emit('save')

    # def redrawDiagram(self):
    #     print("Stub: Redraw the entire diagram")

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

        # # Button for Clear
        # btnClear = QPushButton("Clear")
        # btnClear.clicked.connect(self.clearAction)
        # layout.addWidget(btnClear)

        dialog.setLayout(layout)
        dialog.exec()

    ### EDIT ACTION STUBS

    def undoAction(self):
        print("Stub: Undo the last action")

    def redoAction(self):
        print("Stub: Redo the last undone action")

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

    def newClassAction(self):
        dialog = NewClassDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name = dialog.getClassname()
            classCard = ClassCard(class_name)
            self.diagramArea.addClassCard(classCard, class_name)
            self._process_task_signal.emit('class -a ' + class_name, self)
        
    def deleteClassAction(self): 
        class_names = [entity._name for entity in self._diagram._entities]
        dialog = DeleteClassDialog(class_names, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_class_name = dialog.getSelectedClass()
            self.diagramArea.removeClassCard(selected_class_name)
            self._process_task_signal.emit('class -d ' + selected_class_name, self)
                

    def renameClassAction(self):
        class_names = [entity._name for entity in self._diagram._entities]
        dialog = RenameClassDialog(class_names, self)   
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_class_name = dialog.getSelectedClass()
        new_class_name = dialog.getNewClassName()
        if new_class_name and new_class_name not in class_names:
            self._process_task_signal.emit(f'class -r {selected_class_name} {new_class_name}', self)
            self.diagramArea.renameClassCard(selected_class_name, new_class_name)
        else:
            QMessageBox.warning(self, "Rename Class", "Invalid new class name or name already exists.")
         
    

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

        btnChangeParams = QPushButton("Change Parameters")
        btnChangeParams.clicked.connect(self.changeMethodParamsAction)
        layout.addWidget(btnChangeParams)

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
       
        class_names = [entity._name for entity in self._diagram._entities]
        return_types = ["void", "int", "string", "bool", "float"]

        dialog = AddMethodDialog(class_names, return_types, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, method_name, params, return_type = dialog.getMethodInfo()
            
            if method_name:  # Basic validation
                self._process_task_signal.emit(f'mthd -a {class_name} {method_name} {return_type}', self)
                for classCard in self.diagramArea.findChildren(ClassCard):
                    if classCard._name == class_name:
                        classCard.add_method(f"{method_name} : {return_type}")
                        break
            else:
                QMessageBox.warning(self, "Error", "Method name cannot be empty.")

    def removeMethodAction(self):
        classes_with_methods = {
            classCard._name: classCard.getMethods()
            for classCard in self.diagramArea.findChildren(ClassCard)
        }

        dialog = RemoveMethodDialog(classes_with_methods, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, method_name_and_type = dialog.getSelection()
            method_name = method_name_and_type.split(": ")[0]  
            
            self._process_task_signal.emit(f'mthd -d {class_name} {method_name}', self)
            for class_card in self.findChildren(ClassCard):
                if class_card._name == class_name:
                    class_card.remove_method(method_name_and_type)
                    break


    def renameMethodAction(self):
        classes_with_methods = {
            classCard._name: classCard.getMethods()
            for classCard in self.diagramArea.findChildren(ClassCard)
        }
           # Create and show the dialog
        dialog = RenameMethodDialog(classes_with_methods, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, old_method_name_and_type, new_method_name = dialog.getSelection()
            old_method_name = old_method_name_and_type.split(" : ")[0]  

            # Check for basic validation
            if new_method_name:
                self._process_task_signal.emit(f'mthd -r {class_name} {old_method_name} {new_method_name}', self)
                for classCard in self.diagramArea.findChildren(ClassCard):
                    if classCard._name == class_name:
                        classCard.rename_method(old_method_name, new_method_name)
                        break
            else:
                QMessageBox.warning(self, "Error", "New method name cannot be empty.")
                
    def addFieldAction(self):
        # Pass the list of class names to the dialog
        dialog = AddFieldDialog(self.class_names, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, field_name, field_type = dialog.getFieldInfo()
            if class_name and field_name and field_type:
                print(f"Adding field: {field_name} with type: {field_type} to class {class_name}")
                # Proceed with adding the field to the selected class
            else:
                print("Class name, field name, and type cannot be empty.")

    def removeFieldAction(self):
        # Similar update for RemoveFieldDialog...
        dialog = RemoveFieldDialog(self.class_names, self.fields, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, selected_field = dialog.getSelectedField()
            print(f"Removing field: {selected_field} from class {class_name}")
            # Proceed with removing the field from the selected class


    def renameFieldAction(self):
        # Similar update for RenameFieldDialog...
        dialog = RenameFieldDialog(self.class_names, self.fields, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, original_field_name, new_field_name = dialog.getFieldSelection()
            if class_name and not new_field_name:
                print("The new field name cannot be empty.")
                return
            if new_field_name in fields:
                print("A field with this name already exists in the selected class.")
                return

            print(f"Renaming field '{original_field_name}' to '{new_field_name}' in class {class_name}")
            # Proceed with renaming the field in the selected class


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
        # Assuming 'classes' is a list of class names available for creating relationships
        classes = ["ClassA", "ClassB", "ClassC", "ClassD"]

        dialog = CreateRelationshipDialog(classes, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            src_class, dest_class, relationship_type = dialog.getRelationshipInfo()
            print(f"Creating {relationship_type} relationship from {src_class} to {dest_class}")
            # TODO Here, you would add the relationship to your model or data structure

    def removeRelationshipAction(self):
        # Assuming 'existing_relationships' is a list of strings representing current relationships
        # Each string could be formatted as "SourceClass -> DestinationClass: RelationshipType"
        existing_relationships = [
            "ClassA -> ClassB: Aggregation",
            "ClassB -> ClassC: Composition",
            "ClassC -> ClassD: Inheritance",
            "ClassD -> ClassA: Realization"
        ]

        dialog = RemoveRelationshipDialog(existing_relationships, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_relationship = dialog.getSelectedRelationship()
            print(f"Removing relationship: {selected_relationship}")
            # TODO Here, remove the selected relationship from your model or data structure

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
        ##TODO

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

    def changeMethodParamsAction(self):
        dialog = ChangeParamsDialog(self.classes_methods_params, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            className, methodName, newParams, paramsToRemove = dialog.getChanges()

            # Here, you'll need to implement how to add new parameters and remove selected ones.
            # This might involve updating a model, a database, or directly manipulating code.

            print(f"Class: {className}, Method: {methodName}")
            print(f"Adding parameters: {newParams}")
            print(f"Removing parameters: {paramsToRemove}")

            # Example: Update method parameters in the backend
            # self.backend.updateMethodParams(className, methodName, newParams, paramsToRemove)

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


class DiagramArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.classCards = {}  # Dictionary to track class cards
        self.lastCardPosition = QPoint(10, 10)  # Initial position for the first card
        self.offsetIncrement = QPoint(15, 15)  # Offset for the next card position

    def initUI(self):
        self.setFixedSize(650, 850)  # Adjust size as necessary
        self.setStyleSheet("background-color: white;")

    def addClassCard(self, classCard, className):
        classCard.setParent(self)
        classCard.move(self.lastCardPosition)
        classCard.show()
        self.lastCardPosition += self.offsetIncrement
        if self.lastCardPosition.x() > self.width() - 100 or self.lastCardPosition.y() > self.height() - 100:
            self.lastCardPosition = QPoint(10, 10)
        self.classCards[className] = classCard  # Store the class card with its name as the key

    def removeClassCard(self, className):
        if className in self.classCards:
            classCard = self.classCards.pop(className)  
            classCard.deleteLater() 
            
    def renameClassCard(self, old_name, new_name):
    # Find the class card widget with the old_name
        for classCard in self.findChildren(ClassCard):
            if classCard._name == old_name:
                classCard.set_name(new_name)  


if __name__ == "__main__":
    app = QApplication([])

    gui = GUIV2()
    gui.show()
    app.exec()
