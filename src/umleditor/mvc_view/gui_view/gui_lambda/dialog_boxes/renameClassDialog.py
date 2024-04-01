from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton

class RenameClassDialog(QDialog):
    def __init__(self, class_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename Class")
        self.class_names = class_names

        self.layout = QVBoxLayout(self)

        # Class selection
        self.layout.addWidget(QLabel("Select a class to rename:"))
        self.comboBox = QComboBox()
        self.comboBox.addItems(self.class_names)
        self.layout.addWidget(self.comboBox)

        # New name input
        self.layout.addWidget(QLabel("New class name:"))
        self.newNameLineEdit = QLineEdit()
        self.layout.addWidget(self.newNameLineEdit)

        # Rename button
        self.renameButton = QPushButton("Rename")
        self.layout.addWidget(self.renameButton)
        self.renameButton.clicked.connect(self.accept)

        # Cancel button
        self.cancelButton = QPushButton("Cancel")
        self.layout.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.reject)

    def getSelectedClass(self):
        return self.comboBox.currentText()

    def getNewClassName(self):
        return self.newNameLineEdit.text().strip()
