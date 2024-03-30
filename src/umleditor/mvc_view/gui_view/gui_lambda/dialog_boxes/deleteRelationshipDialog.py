from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton


class RemoveRelationshipDialog(QDialog):
    def __init__(self, relationships, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Remove Relationship")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Select a relationship to remove:"))
        self.relationshipComboBox = QComboBox(self)
        # Format: "SourceClass -> DestinationClass: RelationshipType"
        self.relationshipComboBox.addItems(relationships)  # Assuming relationships are properly formatted strings
        layout.addWidget(self.relationshipComboBox)

        removeButton = QPushButton("Remove", self)
        removeButton.clicked.connect(self.accept)
        layout.addWidget(removeButton)

        cancelButton = QPushButton("Cancel", self)
        cancelButton.clicked.connect(self.reject)
        layout.addWidget(cancelButton)

    def getSelectedRelationship(self):
        return self.relationshipComboBox.currentText()
