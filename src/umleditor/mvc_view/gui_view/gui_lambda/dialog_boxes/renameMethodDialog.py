from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout


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


        # Buttons layout
        buttonsLayout = QHBoxLayout()
        renameButton = QPushButton("Rename", self)
        renameButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(renameButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

        layout.addLayout(buttonsLayout)

    def getMethodSelection(self):
        return self.methodComboBox.currentText(), self.newNameLineEdit.text().strip(), self.parametersLineEdit.text().strip()
