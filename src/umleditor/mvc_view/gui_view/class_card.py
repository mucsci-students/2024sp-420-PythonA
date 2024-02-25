from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit, QLabel, QListWidgetItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal

class ClassCard(QWidget):
    """
    ClassCard - Widget representing a class in the UML diagram editor.

    Signals:
        _process_task_signal (str, QWidget): Signal triggered for task processing.
        _enable_widgets_signal (bool, QWidget): Signal triggered to enable/disable widget interactions.
    """
    _process_task_signal = pyqtSignal(str, QWidget)
    _enable_widgets_signal = pyqtSignal(bool, QWidget)

    def __init__(self, name: str):
        """
        Initializes the ClassCard widget.

        Args:
            name (str): The name of the class.
        """
        super().__init__()
        self.set_name(name)
        self.initUI()
    
    def set_name(self, name: str):
        """
        Sets the name of the class.

        Args:
            name (str): The name of the class.
        """
        self._name = name

    def initUI(self):
        """
        Initializes the user interface of the ClassCard widget.
        """
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
        """
        Connects right-click context menus for class label and lists.
        """
        # Connect class label
        self._class_label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._class_label.customContextMenuRequested.connect(self.show_class_menu)
        # Connect field list
        self._list_field.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_field.customContextMenuRequested.connect(self.show_field_menu)

    def set_styles(self):
        """
        Sets styles for the widgets.
        """
        # Set border style for list widgets
        self._list_field.setStyleSheet("border: 1px solid black; border-top: none")
        self._list_method.setStyleSheet("border: 1px solid black; border-bottom: none; border-top: none;")
        self._list_relation.setStyleSheet("border: 1px solid black;")
        # Set style for class label
        self._class_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._class_label.setMinimumHeight(30)
        # Set style for entire widget
        self.setStyleSheet("background-color: white;")

    def show_class_menu(self, position):
        """
        Shows the context menu for the class label.

        Args:
            position: The position of the context menu.
        """
        menu = QMenu()
        field_action = QAction("Add Field", self)
        field_action.triggered.connect(self.add_field_clicked)
        menu.addAction(field_action)
        menu.exec(self._class_label.mapToGlobal(position))

    def show_field_menu(self, position):
        """
        Shows the context menu for the field list.

        Args:
            position: The position of the context menu.
        """
        pass
    
    def add_field_clicked(self):
        """
        Adds a field when the "Add Field" action is clicked.
        """
        # Disables unselected interactions
        self._enable_widgets_signal.emit(False, self)
        # Create field and add to list
        item = QListWidgetItem()
        self._list_field.addItem(item)
        field_text = QLineEdit()
        self._selected_line = field_text
        # lambda ensures text is only evaluated on enter
        field_text.returnPressed.connect(lambda: self.verify_input(field_text.text(), field_text))
        # Formatting / Style
        field_text.setStyleSheet("background-color: #ADD8E6;")
        self._list_field.setItemWidget(item, field_text)
        field_text.setPlaceholderText("Enter Field Here")
        field_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        field_text.setFocus()
    
    def disable_unselected_items(self):
        """
        Disables context menus for all items within the ClassCard
        """
        self._class_label.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._list_field.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._list_method.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._list_relation.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

    def enable_all_items(self):
        """
        Enables context menus for all items within the ClassCard
        """
        self._class_label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_field.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_method.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_relation.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def verify_input(self, input: str, widget: QWidget):
        """
        Sends a signal for the task to be processed.

        Args:
            input (str): The input text.
            widget (QWidget): The associated ClassCard widget.
        """
        task = "fld -a " + self._class_label.text() + " " + input
        self._process_task_signal.emit(task, self)

    def get_selected_line(self):
        """
        Return the currently selected line.

        Returns:
            QLineEdit: The currently selected line.
        """
        return self._selected_line


    def get_task_signal(self):
        """
        Return the task signal to be connected.

        Returns:
            pyqtSignal: The signal for task processing.
        """
        return self._process_task_signal
    
    def get_enable_signal(self):
        """
        Return the enable signal to be connected.

        Returns:
            pyqtSignal: The signal for widget enabling.
        """
        return self._enable_widgets_signal