from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

class ClassCard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create list widget
        self.list_field = QListWidget()
        self.list_method = QListWidget()
        self.list_relation = QListWidget()
        self.list_field.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_field.customContextMenuRequested.connect(self.show_field_menu)
        #self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        #self.list_widget.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.list_field)
        layout.addWidget(self.list_method)
        layout.addWidget(self.list_relation)

        self.setLayout(layout)

        self.setFixedSize(100,200)
        # Add some initial items to the list
        #for i in range(5):
        #    self.list_widget.addItem(f"Item {i}")
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