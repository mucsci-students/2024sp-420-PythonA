from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QListWidget, QListWidgetItem, \
    QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt


class ChangeParamsDialog(QDialog):
    def __init__(self, classes_methods_params, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Method Parameters")

        self.classes_methods_params = classes_methods_params

        layout = QVBoxLayout(self)

        # Class selection
        self.classComboBox = QComboBox()
        self.classComboBox.addItems(sorted(classes_methods_params.keys()))
        layout.addWidget(QLabel("Select Class:"))
        layout.addWidget(self.classComboBox)

        # Method selection
        self.methodComboBox = QComboBox()
        layout.addWidget(QLabel("Select Method:"))
        layout.addWidget(self.methodComboBox)

        self.classComboBox.currentIndexChanged.connect(
            self.updateMethods)  # Connect signal to update method combo box when class changes

        # Parameters input for adding new parameters
        self.newParamsLineEdit = QLineEdit()
        layout.addWidget(QLabel("Add New Parameters (comma-separated):"))
        layout.addWidget(self.newParamsLineEdit)

        # ListWidget for existing parameters with multi-selection
        layout.addWidget(QLabel("Select Parameters to Remove:"))
        self.paramList = QListWidget()
        self.paramList.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.paramList)

        self.methodComboBox.currentIndexChanged.connect(self.updateParams)  # Update parameter list when method changes

        # Buttons for actions
        buttonsLayout = QHBoxLayout()
        changeButton = QPushButton("Change")
        changeButton.clicked.connect(self.accept)
        buttonsLayout.addWidget(changeButton)

        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.reject)
        buttonsLayout.addWidget(cancelButton)

        layout.addLayout(buttonsLayout)

        self.updateMethods()  # Initial update for methods

    def updateMethods(self):
        className = self.classComboBox.currentText()
        methods = self.classes_methods_params.get(className, {})
        self.methodComboBox.clear()
        self.methodComboBox.addItems(sorted(methods.keys()))
        self.updateParams()

    def updateParams(self):
        className = self.classComboBox.currentText()
        methodName = self.methodComboBox.currentText()
        params = self.classes_methods_params.get(className, {}).get(methodName, [])
        self.paramList.clear()  # Clear the list before adding new items
        for param in params:
            item = QListWidgetItem(param)
            self.paramList.addItem(item)

    def getChanges(self):
        className = self.classComboBox.currentText()
        methodName = self.methodComboBox.currentText()
        newParams = [param.strip() for param in self.newParamsLineEdit.text().split(',') if param.strip()]
        selectedParamsToRemove = [self.paramList.item(i).text() for i in range(self.paramList.count()) if
                                  self.paramList.item(i).isSelected()]
        return className, methodName, newParams, selectedParamsToRemove
