from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit, QLabel, QListWidgetItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal


class ClassCard(QWidget):
    # Signal triggered for task processing
    _process_task_signal = pyqtSignal(str)
    def __init__(self, name: str):
        super().__init__()
        self.set_name(name)
        self.initUI()
    
    def set_name(self, name: str):
        self._name = name

    def initUI(self):
        # Container for all of our individual widgets
        layout = QVBoxLayout()

        # Class label
        self._class_label = QLabel(self._name)
        self._class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create list widgets
        self._list_field = QListWidget()
        self._list_method = QListWidget()
        self._list_relation = QListWidget()

        # Connect right click
        self.connect_menus()

        # Add Widgets to class card
        layout.addWidget(self._class_label)
        layout.addWidget(self._list_field)
        layout.addWidget(self._list_method)
        layout.addWidget(self._list_relation)

        #Set styles
        self.set_styles()

        # Size and spacing
        layout.setSpacing(0)
        self.setFixedSize(150,200)

        self.setLayout(layout)

    def connect_menus(self):
        # Connect class label
        self._class_label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._class_label.customContextMenuRequested.connect(self.show_class_menu)
        # Connect field list
        self._list_field.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_field.customContextMenuRequested.connect(self.show_field_menu)

    def set_styles(self):
        # Set border style for list widgets
        self._list_field.setStyleSheet("border: 1px solid black; border-top: none")
        self._list_method.setStyleSheet("border: 1px solid black; border-bottom: none; border-top: none;")
        self._list_relation.setStyleSheet("border: 1px solid black;")
        # Set style for class label
        self._class_label.setStyleSheet("background-color: powderblue; border: 1px solid black;")
        self._class_label.setMinimumHeight(30)
        # Set style for entire widget
        self.setStyleSheet("background-color: white;")

    def show_class_menu(self, position):
        print("Class menu selected")
        menu = QMenu()
        field_action = QAction("Add Field", self)
        field_action.triggered.connect(self.add_field_clicked)
        menu.addAction(field_action)
        menu.exec(self._class_label.mapToGlobal(position))

    def show_field_menu(self, position):
        print("Field List selected")
    
    def add_field_clicked(self):
        # Create new field 
        item = QListWidgetItem()
        self._list_field.addItem(item)
        field_text = QLineEdit()
        # lambda ensures text is only evaluated on enter
        field_text.returnPressed.connect(lambda: self.verify_input(field_text.text()))
        self._list_field.setItemWidget(item, field_text)
        field_text.setPlaceholderText("Enter Field Here")
        field_text.setFocus()
        print("Add field action clicked")

    def verify_input(self, input):
        self._process_task_signal.emit(input)
        print("Return key pressed")

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