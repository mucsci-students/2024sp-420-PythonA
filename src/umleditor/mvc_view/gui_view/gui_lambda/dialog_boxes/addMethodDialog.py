from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout


class AddMethodDialog(QDialog):
    def __init__(self, classes, return_types, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Method")

        layout = QVBoxLayout(self)

        # Class selection
        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(classes)  # Populate with class names
        layout.addWidget(self.classComboBox)

        # Method name input
        layout.addWidget(QLabel("Method Name:"))
        self.methodNameLineEdit = QLineEdit(self)
        layout.addWidget(self.methodNameLineEdit)

        # Method parameters input with instructions for comma-separated values
        paramsLabel = QLabel("Parameters (optional, separate by commas):")
        layout.addWidget(paramsLabel)
        self.parametersLineEdit = QLineEdit(self)
        layout.addWidget(self.parametersLineEdit)

        # Return type selection
        layout.addWidget(QLabel("Return Type:"))
        self.returnTypeComboBox = QComboBox(self)
        self.returnTypeComboBox.addItems(return_types)  # Populate with possible return types
        layout.addWidget(self.returnTypeComboBox)

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        addButton = QPushButton("Add", self)
        addButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(addButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

        layout.addLayout(buttonsLayout)

    def getMethodInfo(self):
        # Return information as is, caller will handle splitting parameters if needed
        return (self.classComboBox.currentText(), self.methodNameLineEdit.text(),
                self.parametersLineEdit.text(), self.returnTypeComboBox.currentText())

