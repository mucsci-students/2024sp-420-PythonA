from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton


class CreateRelationshipDialog(QDialog):
    def __init__(self, classes, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Relationship")

        layout = QVBoxLayout(self)

        # Source class selection
        layout.addWidget(QLabel("Source Class:"))
        self.srcClassComboBox = QComboBox(self)
        self.srcClassComboBox.addItems(classes)  # Populate with class names
        layout.addWidget(self.srcClassComboBox)

        # Destination class selection
        layout.addWidget(QLabel("Destination Class:"))
        self.destClassComboBox = QComboBox(self)
        self.destClassComboBox.addItems(classes)  # Populate with class names
        layout.addWidget(self.destClassComboBox)

        # Relationship type selection
        layout.addWidget(QLabel("Relationship Type:"))
        self.relationshipTypeComboBox = QComboBox(self)
        relationship_types = ["Aggregation", "Composition", "Inheritance", "Realization"]
        self.relationshipTypeComboBox.addItems(relationship_types)
        layout.addWidget(self.relationshipTypeComboBox)

        # Create button
        createButton = QPushButton("Create", self)
        createButton.clicked.connect(self.accept)
        layout.addWidget(createButton)

        # Cancel button
        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getRelationshipInfo(self):
        return (self.srcClassComboBox.currentText(), self.destClassComboBox.currentText(),
                self.relationshipTypeComboBox.currentText())
