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
        # Create menu & Actions
        menu = QMenu()
        field_action = QAction("Add Field", self)
        # TODO method_action = QAction("Add Method", self)
        relation_action = QAction("Add Relation", self)

        menu.addAction(field_action)
        # TODO menu.addAction(method_action)
        menu.addAction(relation_action)

        # Add button functionality
        field_action.triggered.connect(lambda: self.menu_action_clicked(self._list_field, "Enter Field"))
        # TODO method_action.triggered.connect(lambda: self.menu_action_clicked(self._list_method, "e.g. add(int, int)"))
        relation_action.triggered.connect(lambda: self.menu_action_clicked(self._list_relation, "e.g. src dst type"))
        # Create Menu
        menu.exec(self.mapToGlobal(position))

    def show_row_menu(self, position, widget: QLineEdit):
        """
        Shows the edit/delete menu for QLineEdit based selections

        Args:
            position: The position of the context menu.
        """
        # Create menu & Actions
        menu = QMenu()
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)
        menu.addAction(edit_action)
        menu.addAction(delete_action)

        # Add button functionality
        edit_action.triggered.connect(lambda: self.edit_action_clicked(widget))
        delete_action.triggered.connect(lambda: self.delete_action_clicked(widget))

        # Map the position to global coordinates
        global_position = widget.mapToGlobal(position)

        # Create Menu
        menu.exec(global_position)
    
    def edit_action_clicked(self, widget: QLineEdit):
        """
        Prepares a QLineEdit widget for editing.

        Args:
            widget (QLineEdit): The QLineEdit widget to be edited.

        Returns:
            None
        """
        # Update selected widget
        self._selected_line = widget
        # Disables unselected interactions
        self._enable_widgets_signal.emit(False, self) 
        self._old_text = widget.text()
        self.enable_context_menus(False)
        widget.setStyleSheet("background-color: #ADD8E6;")
        widget.setReadOnly(False)
        widget.setFocus()
    
    def delete_action_clicked(self, widget: QLineEdit):
        """
        Removes the given QLineEdit widget from its parent QListWidget.

        Args:
            widget (QLineEdit): The QLineEdit widget to be removed.
        """
        # Delete field from diagram
        self._process_task_signal.emit("fld -d " + self._class_label.text() + " " + widget.text(), self)

        lists = [(self._list_field, self._list_field.count()),
                (self._list_relation, self._list_relation.count()),
                (self._list_method, self._list_method.count())]

        for list_widget, count in lists:
            for index in range(count):
                item = list_widget.item(index)
                if item is not None:
                    line_edit = list_widget.itemWidget(item)
                    if line_edit == widget:
                        list_widget.removeItemWidget(item)
                        list_widget.takeItem(index)
                        return
        


    
    def unselected_state(self):
        """
        Returns the Class Card and all widgets to an unselected state
        """
        self._enable_widgets_signal.emit(True, self) 
        self.enable_context_menus(True)
        self._selected_line.setReadOnly(True)
        self._selected_line.setStyleSheet("background-color: white;")


    def menu_action_clicked(self, list: QListWidget, placeholder: str):
        """
        Adds a field when the "Add ____" action is clicked.
        """
        # Disables unselected interactions
        self._enable_widgets_signal.emit(False, self)   

        # Create field and add to list
        item = QListWidgetItem()
        list.addItem(item) #!!!
        text = QLineEdit()
        self._selected_line = text
        text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Set old_text as blank
        self._old_text = ""

        # Pass the QLineEdit instance 
        text.customContextMenuRequested.connect(lambda pos: self.show_row_menu(pos, text))

        # lambda ensures text is only evaluated on enter
        text.returnPressed.connect(lambda: self.verify_input(text.text(), list))

        # Formatting / Style
        text.setStyleSheet("background-color: #ADD8E6;")
        list.setItemWidget(item, text)
        text.setPlaceholderText(placeholder)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Disable all context menus while actively editing
        self.enable_context_menus(False)
    
    def enable_context_menus(self, enable: bool):
        """
        Enable/disable context menus for all items within the ClassCard
        """
        stack = [self]
        while stack:
            current_widget = stack.pop()
            if enable:
                current_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  
            else:
                current_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)  
            if isinstance(current_widget, QWidget):
                stack.extend(current_widget.findChildren(QWidget))

    def verify_input(self, new_text: str, list: QListWidget):
        """
        Sends a signal for the task to be processed.

        Args:
            input (str): The input text.
            widget (QWidget): The associated ClassCard widget.
        """
        if list == self._list_field:
            if self._old_text == "":
                self._process_task_signal.emit("fld -a " + self._class_label.text() + " " + new_text, self)
            else:
                self._process_task_signal.emit("fld -r " + self._class_label.text() + " " + self._old_text + " " + new_text, self)

        elif list == self._list_relation:
            if self._old_text == "":
                words = self.split_relation(new_text)
                self._process_task_signal.emit("rel -a " + words[0] + " " + words[1] + " " + words[2], self)
            else:
                self._process_task_signal.emit("rel -e " +  self._old_text + " " + new_text, self)
    
    def split_relation(self, text: str):
        words = text.split()
        while len(words) < 3:
            words.append("")  
        return words

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