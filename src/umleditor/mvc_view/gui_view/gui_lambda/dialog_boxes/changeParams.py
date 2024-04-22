from PyQt6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDialogButtonBox, QApplication, QWidget

class ChangeParamsDialog(QDialog):
    def __init__(self, classes_methods_params, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Method Parameters")
        self.classes_methods_params = classes_methods_params  # This would ideally be a dict or list
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Creating input fields
        self.class_name_edit = QLineEdit(self)
        self.method_name_edit = QLineEdit(self)
        self.params_add_edit = QLineEdit(self)
        self.params_remove_edit = QLineEdit(self)

        # Adding widgets to layout
        layout.addWidget(QLabel("Class Name:"))
        layout.addWidget(self.class_name_edit)
        layout.addWidget(QLabel("Method Name:"))
        layout.addWidget(self.method_name_edit)
        layout.addWidget(QLabel("Parameters to Add (comma-separated):"))
        layout.addWidget(self.params_add_edit)
        layout.addWidget(QLabel("Parameters to Remove (comma-separated):"))
        layout.addWidget(self.params_remove_edit)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getChanges(self):
        # Retrieve data from the dialog
        class_name = self.class_name_edit.text()
        method_name = self.method_name_edit.text()
        params_to_add = self.params_add_edit.text()
        params_to_remove = self.params_remove_edit.text()
        return class_name, method_name, params_to_add, params_to_remove