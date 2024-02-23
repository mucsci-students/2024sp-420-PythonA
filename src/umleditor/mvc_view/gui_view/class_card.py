from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit, QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

class ClassCard(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self.set_name(name)
        self.initUI()
    
    def set_name(self, name: str):
        self._name = name

    def initUI(self):
        layout = QVBoxLayout()

        # Class label
        self._class_label = QLabel(self._name)
        self._class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Create list widgets
        self._list_field = QListWidget()
        self._list_method = QListWidget()
        self._list_relation = QListWidget()
        # Connect right click
        self._list_field.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_field.customContextMenuRequested.connect(self.show_field_menu)

        # Add Widgets to class card
        layout.addWidget(self._class_label)
        layout.addWidget(self._list_field)
        layout.addWidget(self._list_method)
        layout.addWidget(self._list_relation)

        # Set border style for list widgets
        self._list_field.setStyleSheet("border: 1px solid black;")
        self._list_method.setStyleSheet("border: 1px solid black; border-bottom: none; border-top: none;")
        self._list_relation.setStyleSheet("border: 1px solid black;")

        # Set style for class label
        self._class_label.setStyleSheet("background-color: powderblue;")
        self._class_label.setMinimumHeight(30)

        layout.setSpacing(0)
        self.setLayout(layout)
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(150,200)

    def show_field_menu(self, position):

        print("Field List selected")
'''
    def showContextMenu(self, position):
        item = self.list_widget.itemAt(position)
        if item is not None:
            menu = QMenu()
            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(lambda: self.editItem(item))
            menu.addAction(edit_action)
            menu.exec(self.list_widget.mapToGlobal(position))

    def editItem(self, item):
        index = self.list_widget.row(item)
        print(item.text())
'''