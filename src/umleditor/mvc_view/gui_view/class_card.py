from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

class ClassCard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Create list widget
        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.showContextMenu)
        self.layout.addWidget(self.list_widget)

        self.setLayout(self.layout)

        # Add some initial items to the list
        for i in range(5):
            self.list_widget.addItem(f"Item {i}")

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