from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton

class VersionSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select GUI Version")
        layout = QVBoxLayout()

        self.gui_v1_button = QPushButton("Gui V1")
        self.gui_v1_button.clicked.connect(self.select_v1)
        layout.addWidget(self.gui_v1_button)

        self.gui_v2_button = QPushButton("Gui V2")
        self.gui_v2_button.clicked.connect(self.select_v2)
        layout.addWidget(self.gui_v2_button)

        self.gui_v2_button = QPushButton("Gui V2.5")
        self.gui_v2_button.clicked.connect(self.select_v3)
        layout.addWidget(self.gui_v2_button)


        self.setLayout(layout)
        self.selected_version = None

    def select_v1(self):
        self.selected_version = '1'
        self.accept()

    def select_v2(self):
        self.selected_version = '2'
        self.accept()

    def select_v3(self):
        self.selected_version = '3'
        self.accept()
