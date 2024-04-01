from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QPushButton, QLabel


class NewClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Class")
        self.layout = QVBoxLayout(self)
        self.inputLineEdit = QLineEdit(self)
        self.inputLineEdit.setPlaceholderText("Enter class name")
        self.layout.addWidget(QLabel("Class name (one word only):"))
        self.layout.addWidget(self.inputLineEdit)
        self.submitButton = QPushButton("Create", self)
        self.layout.addWidget(self.submitButton)

        self.submitButton.clicked.connect(self.onSubmit)
        self.inputLineEdit.textChanged.connect(self.validateInput)
        self.submitButton.setEnabled(False)  # Disable at start

    def validateInput(self):
        text = self.inputLineEdit.text()
        if " " in text or not text:  # Disallow spaces and empty strings
            self.submitButton.setEnabled(False)
        else:
            self.submitButton.setEnabled(True)

    def onSubmit(self):
        self.accept()  # Closes the dialog and sets its result to QDialog.Accepted

    def getClassname(self):
        return self.inputLineEdit.text().strip()  # Return the validated class name
