from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout


class RemoveMethodDialog(QDialog):
    def __init__(self, classes_with_methods, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Method")

        layout = QVBoxLayout(self)

        # Class selection
        layout.addWidget(QLabel("Class:"))
        self.classComboBox = QComboBox(self)
        self.classComboBox.addItems(list(classes_with_methods.keys()))  # Populate with class names
        layout.addWidget(self.classComboBox)

        # Method selection
        layout.addWidget(QLabel("Select a method to remove:"))
        self.methodComboBox = QComboBox(self)
        self.updateMethods(self.classComboBox.currentText(), classes_with_methods)
        layout.addWidget(self.methodComboBox)

        # Update methods when a different class is selected
        self.classComboBox.currentTextChanged.connect(
            lambda: self.updateMethods(self.classComboBox.currentText(), classes_with_methods))

        # Buttons layout
        buttonsLayout = QHBoxLayout()
        removeButton = QPushButton("Remove", self)
        removeButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(removeButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

        layout.addLayout(buttonsLayout)

    def updateMethods(self, class_name, classes_with_methods):
        self.methodComboBox.clear()
        self.methodComboBox.addItems(classes_with_methods.get(class_name, []))

    def getSelection(self):
        return self.classComboBox.currentText(), self.methodComboBox.currentText()
