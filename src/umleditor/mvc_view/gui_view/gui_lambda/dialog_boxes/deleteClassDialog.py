from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox

class DeleteClassDialog(QDialog):
    def __init__(self, classes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Class")
        self.classes = classes
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Select a class to delete:"))

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(self.classes)
        self.layout.addWidget(self.comboBox)

        self.deleteButton = QPushButton("Delete", self)
        self.layout.addWidget(self.deleteButton)
        self.deleteButton.clicked.connect(self.onDelete)

        self.cancelButton = QPushButton("Cancel", self)
        self.layout.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.reject)

    def onDelete(self):
        self.accept()  # Closes the dialog and sets its result to QDialog.Accepted

    def getSelectedClass(self):
        return self.comboBox.currentText()
