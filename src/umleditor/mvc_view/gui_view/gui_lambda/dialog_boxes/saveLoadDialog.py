from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QApplication, QLabel

class SaveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save File")
        self.layout = QVBoxLayout(self)

        # Add a label
        self.label = QLabel("Enter filename:", self)
        self.layout.addWidget(self.label)

        # Add a text edit for the filename
        self.filenameEdit = QLineEdit(self)
        self.layout.addWidget(self.filenameEdit)

        # Add a button for submitting
        self.submitButton = QPushButton("Save", self)
        self.submitButton.clicked.connect(self.accept)
        self.layout.addWidget(self.submitButton)

    def getFilename(self):
        return self.filenameEdit.text()
    
class LoadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load File")
        self.layout = QVBoxLayout(self)

        # Add a label
        self.label = QLabel("Enter filename:", self)
        self.layout.addWidget(self.label)

        # Add a text edit for the filename
        self.filenameEdit = QLineEdit(self)
        self.layout.addWidget(self.filenameEdit)

        # Add a button for submitting
        self.submitButton = QPushButton("Load", self)
        self.submitButton.clicked.connect(self.accept)
        self.layout.addWidget(self.submitButton)

    def getFilename(self):
        return self.filenameEdit.text()