from PyQt6.QtWidgets import  QPushButton, QVBoxLayout, QLineEdit, QDialog, QDialogButtonBox, QLabel
'''
    Custom Dialog Box w/ custom accept signal allowing us to
    check for valid class input
'''
class CustomInputDialog(QDialog):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(name)
        
        self.input_text = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        button_box = QDialogButtonBox()
        button_box.addButton(self.ok_button, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(self.cancel_button, QDialogButtonBox.ButtonRole.RejectRole)

        layout = QVBoxLayout()
        layout.addWidget(self.input_text)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.cancel_button.clicked.connect(self.reject)