from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout


# Dialog for adding a new field
class AddFieldDialog(QDialog):
    def __init__(self, classes, types, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Field")

        layout = QVBoxLayout(self)

        # Class selection
        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(classes)  # Populate with class names
        layout.addWidget(self.classComboBox)

        # Method name input
        layout.addWidget(QLabel("Field Name:"))
        self.fieldNameLineEdit = QLineEdit(self)
        layout.addWidget(self.fieldNameLineEdit)

        # Type selection
        layout.addWidget(QLabel("Type:"))
        self.typeComboBox = QComboBox(self)
        self.typeComboBox.addItems(types)  # Populate with possible types
        layout.addWidget(self.typeComboBox)

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        addButton = QPushButton("Add", self)
        addButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(addButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

        layout.addLayout(buttonsLayout)

    def getFieldInfo(self):
        # Return information as is, caller will handle splitting parameters if needed
        return (self.classComboBox.currentText(), self.fieldNameLineEdit.text(),
                 self.typeComboBox.currentText())



# Dialog for removing an existing field
class RemoveFieldDialog(QDialog):
    def __init__(self, classes_with_fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Fields")

        layout = QVBoxLayout(self)

        # Class selection
        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(list(classes_with_fields.keys()))  # Populate with class names
        layout.addWidget(self.classComboBox)

        # Fields selection
        layout.addWidget(QLabel("Select a field to remove:"))
        self.fieldsComboBox = QComboBox(self)
        self.updateFields(self.classComboBox.currentText(), classes_with_fields)
        layout.addWidget(self.fieldsComboBox)

        # Update fields when a different class is selected
        self.classComboBox.currentTextChanged.connect(
            lambda: self.updateFields(self.classComboBox.currentText(), classes_with_fields))

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        removeButton = QPushButton("Remove", self)
        removeButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(removeButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

        layout.addLayout(buttonsLayout)

    def updateFields(self, class_name, classes_with_fields):
        self.fieldsComboBox.clear()
        self.fieldsComboBox.addItems(classes_with_fields.get(class_name, []))

    def getSelection(self):
        return self.classComboBox.currentText(), self.fieldsComboBox.currentText()


# Dialog for renaming a selected field
class RenameFieldDialog(QDialog):
    def __init__(self, classes_with_fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Field")

        layout = QVBoxLayout(self)

        # Class selection
        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(list(classes_with_fields.keys()))  # Populate with class names
        layout.addWidget(self.classComboBox)

        # Field selection
        layout.addWidget(QLabel("Select a field to rename:"))
        self.fieldComboBox = QComboBox(self)
        self.updateFields(self.classComboBox.currentText(), classes_with_fields)
        layout.addWidget(self.fieldComboBox)

        # New name input
        layout.addWidget(QLabel("New field name:"))
        self.newNameLineEdit = QLineEdit(self)
        layout.addWidget(self.newNameLineEdit)

        # Update methods when a different class is selected
        self.classComboBox.currentTextChanged.connect(
            lambda: self.updateFields(self.classComboBox.currentText(), classes_with_fields))

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        renameButton = QPushButton("Rename", self)
        renameButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(renameButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

        layout.addLayout(buttonsLayout)

    def updateFields(self, class_name, classes_with_fields):
        self.fieldComboBox.clear()
        fields = classes_with_fields.get(class_name, [])
        self.fieldComboBox.addItems(fields)

    def getSelection(self):
        return self.classComboBox.currentText(), self.fieldComboBox.currentText(), self.newNameLineEdit.text().strip()