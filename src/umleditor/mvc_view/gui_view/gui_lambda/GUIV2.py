import os

from umleditor.mvc_model.diagram import Diagram
from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QUrl
from PyQt6.QtWidgets import (QDialog, QMainWindow, QWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout,
                             QMessageBox, QHBoxLayout, QRadioButton, QDialogButtonBox, QListWidget, QLabel, QFrame,
                             QFileDialog)
from PyQt6.QtGui import QAction, QPainter, QPen, QColor,QDesktopServices
from umleditor.mvc_view.gui_view.gui_lambda.diagram_area import DiagramArea
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.newClassDialog import NewClassDialog
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.deleteClassDialog import DeleteClassDialog
from umleditor.mvc_view.gui_view.gui_lambda.class_card_revamp import ClassCard
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
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.saveLoadDialog import SaveDialog, LoadDialog
import sys


class GUIV2(QMainWindow):
    _process_task_signal = pyqtSignal(str, QWidget)
    close_signal = pyqtSignal()
    actionNum = 0
    undoNum = 0

    def __init__(self):
            super().__init__()
            self._diagram = Diagram()
            self.diagramArea = DiagramArea()
            self.lstRelationships = QListWidget()
            self.gridLayout = QGridLayout()
            self.sidebarWidget = QWidget()
            self.sidebarLayout = QVBoxLayout(self.sidebarWidget)  # Initialize sidebar layout with sidebarWidget
            self.setWindowTitle("UML Editor - GUI V2")
            self.setGeometry(300, 300, 850, 850)
            self.initUI()


            self.applyDarkTheme()
            self.currentFilePath = " "
            self.classes_methods_params = []

        
    def get_signal(self):
        return self._process_task_signal

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.mainLayout = QHBoxLayout(self.centralWidget)
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


    def setupLayout(self):
        # Main layout for the entire window
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # Removes margins so the page fills the window

        # Initialize DiagramArea and add it directly to the mainLayout
        self.mainLayout.addWidget(self.diagramArea)
        self.mainLayout.setStretchFactor(self.diagramArea, 4)  # Give the diagram area more space compared to the sidebar

        # Setup sidebar part of the layout
        self.setupSidebar(self.centralWidget)  # Use centralWidget as the parent widget for the sidebar


    def setupSidebar(self, mainLayout):
        # Clear existing widgets from sidebarLayout
        for i in reversed(range(self.sidebarLayout.count())):
            widget = self.sidebarLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Define button info with actions
        buttons_info = [
            ("File", self.diagramArea.get_random_color(), self.fileAction),
            ("Save", self.diagramArea.get_random_color(), self.saveFile),
            ("Load", self.diagramArea.get_random_color(), self.openFile),
            ("Undo", self.diagramArea.get_random_color(), self.undoAction),
            ("Redo", self.diagramArea.get_random_color(), self.redoAction),
            ("Add Class", self.diagramArea.get_random_color(), self.newClassAction),
            ("Edit Classes", self.diagramArea.get_random_color(), self.classesAction),
            ("Attributes", self.diagramArea.get_random_color(), self.attributesAction),
            ("Relationships", self.diagramArea.get_random_color(), self.relationshipsAction),
            ("Help", self.diagramArea.get_random_color(), self.helpAction),
        ]

        for text, color, action in buttons_info:
            btn = QPushButton(text)
            if text == "Save" or text == "Edit Classes" or text == "Attributes":
                if len(self._diagram._entities) != 0:
                    btn.setStyleSheet(f"QPushButton {{border: 2px solid {color};}}")
                    btn.clicked.connect(action)
                    self.sidebarLayout.addWidget(btn)
            elif text == "Relationships":
                if len(self._diagram._entities) >= 2:
                    btn.setStyleSheet(f"QPushButton {{border: 2px solid {color};}}")
                    btn.clicked.connect(action)
                    self.sidebarLayout.addWidget(btn)
            elif text == "Undo":
                if self.actionNum > 0:
                    btn.setStyleSheet(f"QPushButton {{border: 2px solid {color};}}")
                    btn.clicked.connect(action)
                    self.sidebarLayout.addWidget(btn)
            elif text == "Redo":
                if self.undoNum > 0:
                    btn.setStyleSheet(f"QPushButton {{border: 2px solid {color};}}")
                    btn.clicked.connect(action)
                    self.sidebarLayout.addWidget(btn)                    
            else:
                btn.setStyleSheet(f"QPushButton {{border: 2px solid {color};}}")
                btn.clicked.connect(action)
                self.sidebarLayout.addWidget(btn)

        lblRelationships = QLabel("")
        lblRelationships.setObjectName("lblRelationships")
        self.sidebarLayout.addWidget(lblRelationships)

        self.lstRelationships = QListWidget()
        self.lstRelationships.setObjectName("lstRelationships")

        rel_list = self._diagram.list_relations()
        for rel in rel_list:
            self.lstRelationships.addItem(rel)

        self.mainLayout.addWidget(self.sidebarWidget)
        self.sidebarWidget.setObjectName("sidebarWidget")

        self.mainLayout.setStretchFactor(self.sidebarWidget, 1)
        

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

        btnSave = QPushButton("Save")
        btnSave.clicked.connect(self.saveFile)
        layout.addWidget(btnSave)
        
        btnExportAsImg = QPushButton("Export as Image")
        btnExportAsImg.clicked.connect(self.exportDiagram)
        layout.addWidget(btnExportAsImg)
        
        

        # btnRedraw = QPushButton("Redraw")
        # btnRedraw.clicked.connect(self.redrawDiagram)
        # layout.addWidget(btnRedraw)

        dialog.setLayout(layout)
        dialog.exec()
    ### FILE ACTION STUBS

    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File")
        if file_name:
            file_name_without_ext, ext = os.path.splitext(file_name)
            if ext.lower() == ".json":
                file_name = os.path.basename(file_name_without_ext)
            self._process_task_signal.emit(f'load {file_name}', self)
            self.refreshGUI()
        
        
    def newFile(self):
        # Logic to reset the application state for a new file
        print("Creating a new file...")
        # Example: Clearing the UI, resetting data models, etc.

    def saveFile(self):
        save_name, _ = QFileDialog.getSaveFileName(self, "Save File")
        if save_name:
            file_name_without_path = os.path.basename(save_name)
            self._process_task_signal.emit(f'save {file_name_without_path}', self)

    def exportDiagram(self):
        # Open a file dialog to select the path for saving the PNG
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "PNG Files (*.png)")
        if filePath:
            self.diagramArea.exportAsImage(filePath)
            QMessageBox.information(self, "Export", "Diagram exported successfully as PNG.")

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

        dialog.setLayout(layout)
        dialog.exec()

    ### EDIT ACTION STUBS

    def undoAction(self):
        self._process_task_signal.emit('undo', self)
        self.refreshGUI()
        self.undoNum += 1
        self.actionNum -= 1
        self.setupSidebar(self.mainLayout)
        self.refreshGUI()
        
        
        

    def redoAction(self):
        self._process_task_signal.emit('redo', self)
        self.refreshGUI()
        self.undoNum -= 1
        self.actionNum += 1
        self.setupSidebar(self.mainLayout)
        self.refreshGUI()
        

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
            if class_name:
                self._process_task_signal.emit('class -a ' + class_name, self)
                entity = self._diagram.get_entity(class_name)
                classCard = ClassCard(class_name, entity)
                self.diagramArea.addClassCard(classCard, class_name)
                self.actionNum += 1
                if len(self._diagram._entities) <= 2:
                    self.setupSidebar(self.mainLayout)
                    self.refreshGUI()
        
    def deleteClassAction(self): 
        class_names = [entity._name for entity in self._diagram._entities]
        dialog = DeleteClassDialog(class_names, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_class_name = dialog.getSelectedClass()
            if selected_class_name:
                self.diagramArea.removeClassCard(selected_class_name)
                self._process_task_signal.emit('class -d ' + selected_class_name, self)
                self.actionNum += 1
                if len(self._diagram._entities) <= 2:
                    self.setupSidebar(self.mainLayout)
                    self.refreshGUI()
                
    def renameClassAction(self):
        class_names = [entity._name for entity in self._diagram._entities]
        dialog = RenameClassDialog(class_names, self)   
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_class_name = dialog.getSelectedClass()
        new_class_name = dialog.getNewClassName()
        if new_class_name and new_class_name not in class_names:
            self.actionNum += 1
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


        methodsLabel = QLabel("Methods")
        layout.addWidget(methodsLabel)

        btnAddMethod = QPushButton("Add Method")
        btnAddMethod.clicked.connect(self.addMethodAction)
        layout.addWidget(btnAddMethod)
        
        for entity in self._diagram._entities:
            if len(entity._methods) != 0:
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
                
        fieldsLabel = QLabel("Fields")
        layout.addWidget(fieldsLabel)

        btnAddField = QPushButton("Add Field")
        btnAddField.clicked.connect(self.addFieldAction)
        layout.addWidget(btnAddField)
        
        for entity in self._diagram._entities:        
            if len(entity._fields) != 0:

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
            class_name, method_name, return_type = dialog.getMethodInfo()
            
            if method_name:  # Basic validation
                self._process_task_signal.emit(f'mthd -a {class_name} {method_name} {return_type}', self)
                for classCard in self.diagramArea.findChildren(ClassCard):
                    if classCard._name == class_name:
                        classCard.add_method(f"{method_name} : {return_type}")
                        self.actionNum += 1
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
            if class_name and method_name:
                self._process_task_signal.emit(f'mthd -d {class_name} {method_name}', self)
                for class_card in self.findChildren(ClassCard):
                    if class_card._name == class_name:
                        class_card.remove_method(method_name_and_type)
                        self.actionNum += 1
                        break

    def renameMethodAction(self):
        classes_with_methods = {
            classCard._name: classCard.getMethods()
            for classCard in self.diagramArea.findChildren(ClassCard)
        }
        dialog = RenameMethodDialog(classes_with_methods, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, old_method_name_and_type, new_method_name = dialog.getSelection()
            old_method_name = old_method_name_and_type.split(" : ")[0]  

            if class_name and old_method_name and new_method_name:
                self._process_task_signal.emit(f'mthd -r {class_name} {old_method_name} {new_method_name}', self)
                for classCard in self.diagramArea.findChildren(ClassCard):
                    if classCard._name == class_name:
                        classCard.rename_method(old_method_name, new_method_name)
                        self.actionNum += 1
                        break
            else:
                QMessageBox.warning(self, "Error", "New method name cannot be empty.")
           
    def changeMethodParamsAction(self):
        dialog = ChangeParamsDialog(self.classes_methods_params, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, method_name, newParams, toRemove = dialog.getChanges()
            newParams = newParams.split(',')
            toRemove = toRemove.split(',')            
            for param in newParams:
                if newParams:
                    self._process_task_signal.emit(f'prm -a {class_name} {method_name} {param}', self)
                    for classCard in self.diagramArea.findChildren(ClassCard):
                        if classCard._name == class_name:
                            classCard.add_param(method_name, param)
                            self.actionNum += 1
                            break
            for param in toRemove:
                if toRemove:
                    self._process_task_signal.emit(f'prm -d {class_name} {method_name} {param}', self)
                    for classCard in self.diagramArea.findChildren(ClassCard):
                        if classCard._name == class_name:
                            classCard.remove_param(method_name, param)
                            self.actionNum += 1
                            break
                
                

    def addFieldAction(self):
        types = ["int", "string", "bool", "float"]
        class_names = [entity._name for entity in self._diagram._entities]
        dialog = AddFieldDialog(class_names, types, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, field_name, type_name = dialog.getFieldInfo()
            
            if field_name: 
                self._process_task_signal.emit(f'fld -a {class_name} {field_name} {type_name}', self)
                for classCard in self.diagramArea.findChildren(ClassCard):
                    if classCard._name == class_name:
                        classCard.add_field(f"{field_name} : {type_name}")
                        self.actionNum += 1
                        break
            else:
                QMessageBox.warning(self, "Error", "Field name cannot be empty.")

    def removeFieldAction(self):
        classes_with_fields = {
            classCard._name: classCard.getFields()
            for classCard in self.diagramArea.findChildren(ClassCard)
        }

        dialog = RemoveFieldDialog(classes_with_fields, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, field_name_and_type = dialog.getSelection()
            field_name = field_name_and_type.split(": ")[0]  
            
            if class_name and field_name:
                self._process_task_signal.emit(f'fld -d {class_name} {field_name}', self)
                for class_card in self.findChildren(ClassCard):
                    if class_card._name == class_name:
                        class_card.remove_field(field_name_and_type)
                        self.actionNum += 1
                        break

    def renameFieldAction(self):
        classes_with_fields = {
            classCard._name: classCard.getFields()
            for classCard in self.diagramArea.findChildren(ClassCard)
        }
        dialog = RenameFieldDialog(classes_with_fields, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            class_name, old_field_name_and_type, new_field_name = dialog.getSelection()
            old_field_name = old_field_name_and_type.split(" : ")[0]  
            
            if class_name and old_field_name:
                
                if new_field_name:
                    self._process_task_signal.emit(f'fld -r {class_name} {old_field_name} {new_field_name}', self)
                    for classCard in self.diagramArea.findChildren(ClassCard):
                        if classCard._name == class_name:
                            classCard.rename_field(old_field_name, new_field_name)
                            self.actionNum += 1
                            break
                else:
                    QMessageBox.warning(self, "Error", "New field name cannot be empty.")

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


    def refreshRelationshipsList(self):
        self.lstRelationships.clear()

        # Assuming _diagram has a method to get all current relationships
        current_relationships = self._diagram.list_relations()
        # Populate the lstRelationships widget with updated relationships
        for relationship in current_relationships:
            self.lstRelationships.addItem(relationship)
            
    def createRelationshipAction(self):
        class_names = [entity._name for entity in self._diagram._entities]
        dialog = CreateRelationshipDialog(class_names, self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            src_class, dest_class, relationship_type = dialog.getRelationshipInfo()
            if src_class and dest_class and relationship_type:
                if src_class != dest_class:
                    self._process_task_signal.emit (f'rel -a {src_class} {dest_class} {relationship_type}', self)
                    self.diagramArea.addRelationship(src_class, dest_class, relationship_type)
                    self.actionNum += 1
                else:
                    QMessageBox.warning(self, "Error", "Source and destination cannot be the same.")
                
                
        self.refreshRelationshipsList()
       
        

    def removeRelationshipAction(self):
        current_relationships = self._diagram.list_relations()
        dialog = RemoveRelationshipDialog(current_relationships, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_relationship = dialog.getSelectedRelationship()

            src_class, type, dest_class = selected_relationship.split(" -> ")

            if src_class and dest_class:
                self._process_task_signal.emit(f'rel -d {src_class} {dest_class}', self)
                self.diagramArea.removeRelationship(src_class, dest_class)
                self.actionNum += 1
            
            self.refreshRelationshipsList()
            
            
                
        

                    
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

        dialog.exec()

    ###STUBS FOR HELP
    def loadReadmeAction(self):
        url = QUrl('https://github.com/mucsci-students/2024sp-420-PythonA#')
        QDesktopServices.openUrl(url)

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
        lblRelationships = self.findChild(QLabel, "lblRelationships")
        if lblRelationships:
            lblRelationships.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
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

    def clearGUI(self):
            self.diagramArea.clearAll() 
            self.lstRelationships.clear()
             
    def refreshGUI(self):
        """Refreshes the entire GUI to reflect the current state."""
        self.clearGUI()
        for class_name in self._diagram._entities:
            name = class_name.get_name()
            classCard = ClassCard(name, class_name)
            self.diagramArea.addClassCard(classCard, name)
            if hasattr(class_name, '_location'):
                classCard.move(QPoint(class_name._location[0], class_name._location[1]))
            else:
                classCard.move(QPoint(10, 10))
            
            for field in class_name._fields:
                field_name, field_type_gen, *rest = field
                try:
                    # Attempt to handle the field type directly if it's not complex
                    if isinstance(field_type_gen, str):
                        field_type = field_type_gen
                    else:
                        # Handle complex types which are represented as strings containing the type
                        field_type = str(field_type_gen).split("'")[1]
                except IndexError:
                    # Log or handle cases where field type is not in the expected format
                    print(f"Error processing field type for {field_name}: {field_type_gen}")
                    continue  # Skip this field or handle as needed

                field_str = f'{field_name} : {field_type}'
                classCard.add_field(field_str)
                    
            for method in class_name._methods:
                method_str = f"{method.get_method_name()} : {method.get_return_type()}"
                classCard.add_method(method_str)
                
        for relation in self._diagram._relations:
            src_class, type, dest_class = str(relation).split(" -> ")
            relationship_str = f"{src_class} -> {dest_class}"
            
            self.refreshRelationshipsList()
            self.diagramArea.addRelationship(src_class, dest_class, type)
            # Updating ClassCard objects with relations
            for classCard in self.diagramArea.findChildren(ClassCard):
                if classCard._name == src_class or classCard._name == dest_class:
                    classCard.add_relation(relationship_str)
                
            self.diagramArea.update()
            self.statusBar().showMessage("GUI Refreshed")
    
        
if __name__ == "__main__":
    app = QApplication([])

    gui = GUIV2()
    gui.show()
    app.exec()
