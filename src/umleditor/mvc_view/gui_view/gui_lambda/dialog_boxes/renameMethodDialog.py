from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton


class RenameMethodDialog(QDialog):
    def __init__(self, methods, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Method")

        layout = QVBoxLayout(self)

        # Method selection
        layout.addWidget(QLabel("Select a method to rename:"))
        self.methodComboBox = QComboBox(self)
        self.methodComboBox.addItems(methods)  # Populate with existing methods
        layout.addWidget(self.methodComboBox)

        # New name input
        layout.addWidget(QLabel("New method name:"))
        self.newNameLineEdit = QLineEdit(self)
        layout.addWidget(self.newNameLineEdit)

        # Rename button
        renameButton = QPushButton("Rename", self)
        renameButton.clicked.connect(self.accept)
        layout.addWidget(renameButton)

        # Cancel button
        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getSelectedMethod(self):
        return self.methodComboBox.currentText()

    def getNewMethodName(self):
        return self.newNameLineEdit.text().strip()
