from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton


class RemoveMethodDialog(QDialog):
    def __init__(self, methods, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Method")

        layout = QVBoxLayout(self)

        # Method selection
        layout.addWidget(QLabel("Select a method to remove:"))
        self.methodComboBox = QComboBox(self)
        self.methodComboBox.addItems(methods)  # Populate with existing methods
        layout.addWidget(self.methodComboBox)

        # Remove button
        removeButton = QPushButton("Remove", self)
        removeButton.clicked.connect(self.accept)
        layout.addWidget(removeButton)

        # Cancel button
        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getSelectedMethod(self):
        return self.methodComboBox.currentText()
