from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton


# Dialog for adding a new field
class AddFieldDialog(QDialog):
    def __init__(self, class_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Field")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(class_names)  # Populate with class names
        layout.addWidget(self.classComboBox)

        layout.addWidget(QLabel("Field Name:"))
        self.fieldNameLineEdit = QLineEdit(self)
        layout.addWidget(self.fieldNameLineEdit)

        layout.addWidget(QLabel("Field Type:"))
        self.fieldTypeLineEdit = QLineEdit(self)
        layout.addWidget(self.fieldTypeLineEdit)

        addButton = QPushButton("Add", self)
        addButton.clicked.connect(self.accept)
        layout.addWidget(addButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getFieldInfo(self):
        return self.classComboBox.currentText(), self.fieldNameLineEdit.text().strip(), self.fieldTypeLineEdit.text().strip()


# Dialog for removing an existing field
class RemoveFieldDialog(QDialog):
    def __init__(self, class_names, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Field")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(class_names)  # Populate with class names
        layout.addWidget(self.classComboBox)


        layout.addWidget(QLabel("Select a field to remove:"))
        self.fieldComboBox = QComboBox(self)
        self.fieldComboBox.addItems(fields)  # Assuming 'fields' is a list of field names
        layout.addWidget(self.fieldComboBox)

        removeButton = QPushButton("Remove", self)
        removeButton.clicked.connect(self.accept)
        layout.addWidget(removeButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getSelectedField(self):
        return self.classComboBox.currentText(), self.fieldComboBox.currentText()


# Dialog for renaming a selected field
class RenameFieldDialog(QDialog):
    def __init__(self, class_names, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Field")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(class_names)  # Populate with class names
        layout.addWidget(self.classComboBox)

        layout.addWidget(QLabel("Select a field to rename:"))
        self.fieldComboBox = QComboBox(self)
        self.fieldComboBox.addItems(fields)
        layout.addWidget(self.fieldComboBox)

        layout.addWidget(QLabel("New field name:"))
        self.newFieldNameLineEdit = QLineEdit(self)
        layout.addWidget(self.newFieldNameLineEdit)

        renameButton = QPushButton("Rename", self)
        renameButton.clicked.connect(self.accept)
        layout.addWidget(renameButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getFieldSelection(self):
        return self.classComboBox.currentText(), self.fieldComboBox.currentText(), self.newFieldNameLineEdit.text().strip()
