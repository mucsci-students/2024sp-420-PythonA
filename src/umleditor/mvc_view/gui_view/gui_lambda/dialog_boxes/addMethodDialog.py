from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton


class AddMethodDialog(QDialog):
    def __init__(self, return_types, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Method")

        layout = QVBoxLayout(self)

        # Method name input
        layout.addWidget(QLabel("Method Name:"))
        self.methodNameLineEdit = QLineEdit(self)
        layout.addWidget(self.methodNameLineEdit)

        # Return type selection
        layout.addWidget(QLabel("Return Type:"))
        self.returnTypeComboBox = QComboBox(self)
        self.returnTypeComboBox.addItems(return_types)  # Populate with possible return types
        layout.addWidget(self.returnTypeComboBox)

        # Add button
        addButton = QPushButton("Add", self)
        addButton.clicked.connect(self.accept)
        layout.addWidget(addButton)

        # Cancel button
        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getMethodInfo(self):
        return self.methodNameLineEdit.text(), self.returnTypeComboBox.currentText()
