from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit, QLabel, QListWidgetItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QPoint
from umleditor.mvc_view.gui_view.gui_cworld.class_input_dialog import CustomInputDialog


class ClassCard(QWidget):
    """
    ClassCard - Widget representing a class in the UML diagram editor.

    Signals:
        _process_task_signal (str, QWidget): Signal triggered for task processing.
        _enable_widgets_signal (bool, QWidget): Signal triggered to enable/disable widget interactions.
    """
    _process_task_signal = pyqtSignal(str, QWidget)
    _enable_widgets_signal = pyqtSignal(bool, QWidget)
    cardMoved = pyqtSignal()

    def __init__(self, name: str):
        """
        Initializes the ClassCard widget.

        Args:
            name (str): The name of the class.
        """
        super().__init__()
        self._name = name
        self.initUI()
        # Used for capturing escape key
        self.installEventFilter(self)
        self.moving = False
        self.offset = None

    

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

        # Set styles
        self.set_styles()

        # Size and spacing
        layout.setSpacing(0)
        self.setFixedSize(150, 200)

        self.setLayout(layout)

    def connect_menus(self):
        """
        Connects right-click context menus for class label and lists.
        """
        # Connect class label
        self._class_label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._class_label.customContextMenuRequested.connect(self.show_class_menu)

    def set_name(self, name: str):
        """
        Sets the name of the class.

        Args:
            name (str): The name of the class.
        """
        self._name = name
        self._class_label.setText(name)
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
        rename_action = QAction("Rename Class", self)
        delete_action = QAction("Delete Class", self)
        field_action = QAction("Add Field", self)
        method_action = QAction("Add Method", self)
        relation_action = QAction("Add Relation", self)

        menu.addAction(rename_action)
        menu.addAction(field_action)
        menu.addAction(method_action)
        menu.addAction(relation_action)
        menu.addSeparator()
        menu.addAction(delete_action)
        # Add button functionality
        delete_action.triggered.connect(self.confirm_delete_class)
        field_action.triggered.connect(lambda: self.menu_action_clicked(self._list_field, "Enter Field"))
        method_action.triggered.connect(
            lambda: self.menu_action_clicked(self._list_method, "e.g. method param1 param2..."))
        relation_action.triggered.connect(lambda: self.menu_action_clicked(self._list_relation, "e.g. dst type"))
        rename_action.triggered.connect(self.rename_action_clicked)

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

        # Save current text within row
        self._old_text = widget.text()

        # Add button functionality
        edit_action.triggered.connect(lambda: self.edit_action_clicked(widget))
        delete_action.triggered.connect(lambda: self.delete_action_clicked(widget))

        # Map the position to global coordinates
        global_position = widget.mapToGlobal(position)

        # Create Menu
        menu.exec(global_position)

    def rename_action_clicked(self):
        self._rename_dialog = CustomInputDialog(name="Rename Class")
        self._rename_dialog.ok_button.clicked.connect(self.confirm_rename_clicked)
        self._rename_dialog.exec()

    def confirm_rename_clicked(self):
        self._process_task_signal.emit("class -r " + self._name + " " + self._rename_dialog.input_text.text(), self)

    def accept_new_name(self, new_name: str):
        self._class_label.setText(new_name)
        self.set_name(new_name)
        self._rename_dialog.reject()

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
        class_name = self._class_label.text()

        lists = [(self._list_field, self._list_field.count()),
                 (self._list_relation, self._list_relation.count()),
                 (self._list_method, self._list_method.count())]

        for list_widget, count in lists:
            for index in range(count):
                item = list_widget.item(index)
                if item is not None:
                    line_edit = list_widget.itemWidget(item)
                    if line_edit == widget:
                        # Call specific delete based on list field
                        if list_widget is self._list_field:
                            self._process_task_signal.emit("fld -d " + class_name + " " + widget.text(), self)
                        elif list_widget is self._list_relation:
                            relation = self.split_relation(widget.text())
                            self._process_task_signal.emit("rel -d " + class_name + " " + relation[0], self)
                        else:
                            method = widget.text().split()
                            self._process_task_signal.emit("mthd -d " + class_name + " " + method[0], self)
                        list_widget.removeItemWidget(item)
                        list_widget.takeItem(index)
                        return
        # Enable widgets/menus
        self._enable_widgets_signal.emit(True, self)
        self.enable_context_menus(True)

    def confirm_delete_class(self):
        """
        Confirms the deletion of the class.
        """
        self._process_task_signal.emit(f"class -d  {self._name}", self)

    def menu_action_clicked(self, list: QListWidget, placeholder: str):
        """
        Adds a field when the "Add ____" action is clicked.
        """
        # Disables unselected interactions
        self._enable_widgets_signal.emit(False, self)

        # Create field and add to list
        item = QListWidgetItem()
        list.addItem(item)  # !!!
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

    def eventFilter(self, obj, event: QEvent):
        """
        Captures escape key inputs and escapes from a selected row

        Args:
            obj: The object for which events are being filtered.
            event (QEvent): The event to be filtered.

        Returns:
            bool: True if the event has been handled, False otherwise.
        """
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                # Handle the escape key press here
                if self._selected_line != None:
                    self.escape_from_row()
                return True
        return super().eventFilter(obj, event)

    def escape_from_row(self):
        """
        Method to escape from row editing mode. If it's a newly added row, removes the row from the class card.
        Otherwise, returns the row to its original state.
        """
        lists = [(self._list_field, self._list_field.count()),
                 (self._list_relation, self._list_relation.count()),
                 (self._list_method, self._list_method.count())]

        # If newly added row, just remove from class card
        if self._old_text == "":
            for list_widget, count in lists:
                for index in range(count):
                    item = list_widget.item(index)
                    if item is not None:
                        line_edit = list_widget.itemWidget(item)
                        if line_edit == self._selected_line:
                            # Call specific delete based on list field
                            list_widget.removeItemWidget(item)
                            list_widget.takeItem(index)
                            break
        # Otherwise return the row to it's original state
        else:
            self._selected_line.setText(self._old_text)

        # Return to unselected state
        self._enable_widgets_signal.emit(True, self)
        self.enable_context_menus(True)
        self._selected_line.setReadOnly(True)
        self._selected_line.setStyleSheet("background-color: white;")

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
        class_name = self._class_label.text()
        # Field task signals
        if list == self._list_field:
            if self._old_text == "":
                self._process_task_signal.emit("fld -a " + class_name + " " + new_text, self)
            else:
                self._process_task_signal.emit("fld -r " + class_name + " " +
                                               self._old_text + " " + new_text, self)
        # Relation task signals - (Source, Destination, Type)
        elif list == self._list_relation:
            if self._old_text == "":
                words = self.split_relation(new_text)
                self._process_task_signal.emit("rel -a " + class_name + " " + " ".join(words), self)
            else:
                self._process_task_signal.emit("rel -e " + class_name + " " + self._old_text + " " +
                                               class_name + " " + new_text, self)
        # Method task signals  
        else:
            # - methodName param1 param2...     
            if self._old_text == "":
                words = new_text.split()
                self._process_task_signal.emit("mthd -ga " + class_name + " " + " ".join(words), self)
            # - oldName newName param1 param2...         
            else:
                words = new_text.split()
                old_name = self._old_text.split()[0]
                self._process_task_signal.emit("mthd -e " + class_name + " " + old_name + " " + " ".join(words), self)
            pass

    def split_relation(self, text: str):
        """
        Splits a string into two words.

        Args:
            text (str): The input string to be split.

        Returns:
            list: A list containing three words. If the input string has fewer than two words,
                  the remaining elements in the list will be empty strings.
        """
        words = text.split()
        while len(words) < 2:
            words.append("")
        return words

    def deselect_line(self):
        """
        Deselects the currently selected QLineEdit.
        """
        self._selected_line = None

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

    #######################################################################

    # load

    def add_field(self, field):
        """
        Adds a field.
        """
        list = self._list_field

        # Create field and add to list
        item = QListWidgetItem()
        list.addItem(item) 
        text = QLineEdit()
        text.setText(field)
        text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Pass the QLineEdit instance 
        text.customContextMenuRequested.connect(lambda pos: self.show_row_menu(pos, text))

        # lambda ensures text is only evaluated on enter
        text.returnPressed.connect(lambda: self.verify_input(text.text(), list))

        # Formatting / Style
        list.setItemWidget(item, text)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text.setReadOnly(True)
        
    def getFields(self):
        """
        Returns a list of fields names added to the class card.
        
        Returns:
            List[str]: A list containing the names of all fields.
        """
        fields = []
        for index in range(self._list_field.count()):
            # Retrieve the QListWidgetItem at the given index
            item = self._list_field.item(index)
            # Assuming the text of each item is the method name
            field_name = self._list_field.itemWidget(item).text()
            fields.append(field_name)
        return fields
        
    def remove_field(self, field_name):
        """
        Removes a field from the class card.

        Args:
            field_name (str): The name of the field to remove.
        """
        for i in range(self._list_field.count()):
            item = self._list_field.item(i)
            line_edit = self._list_field.itemWidget(item)
            if line_edit and line_edit.text() == field_name:
                self._list_field.takeItem(i)
                break
            
    def rename_field(self, old_field_name, new_field_name):
        """
        Renames an existing field in the class card.

        Args:
            old_field_name (str): The current name of the field to be renamed.
            new_field_name (str): The new name for the field.
        """
        for i in range(self._list_field.count()):
            item = self._list_field.item(i)
            line_edit = self._list_field.itemWidget(item)
            if line_edit and line_edit.text().startswith(old_field_name):
                parts = line_edit.text().split(' : ')
                if len(parts) > 1:
                    
                    line_edit.setText(f"{new_field_name}: {parts[1].strip()}")
                else:
                    
                    line_edit.setText(new_field_name)
                break    

    def add_method(self, method):
        """
        Adds a method.
        """
        list = self._list_method

        # Create field and add to list
        item = QListWidgetItem()
        list.addItem(item) 
        text = QLineEdit()
        text.setText(method)
        text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Pass the QLineEdit instance 
        text.customContextMenuRequested.connect(lambda pos: self.show_row_menu(pos, text))

        # lambda ensures text is only evaluated on enter
        text.returnPressed.connect(lambda: self.verify_input(text.text(), list))

        # Formatting / Style
        list.setItemWidget(item, text)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text.setReadOnly(True)
        
    def getMethods(self):
        """
        Returns a list of method names added to the class card.
        
        Returns:
            List[str]: A list containing the names of all methods.
        """
        methods = []
        for index in range(self._list_method.count()):

            item = self._list_method.item(index)
      
            method_name = self._list_method.itemWidget(item).text()
            methods.append(method_name)
        return methods
        
    def remove_method(self, method_name):
        """
        Removes a method from the class card.

        Args:
            method_name (str): The name of the method to remove.
        """
        for i in range(self._list_method.count()):
            item = self._list_method.item(i)
            line_edit = self._list_method.itemWidget(item)
            if line_edit and line_edit.text() == method_name:
                self._list_method.takeItem(i)
                break
    def rename_method(self, old_method_name, new_method_name):
        """
        Renames an existing method in the class card.

        Args:
            old_method_name (str): The current name of the method to be renamed.
            new_method_name (str): The new name for the method.
        """
        for i in range(self._list_method.count()):
            item = self._list_method.item(i)
            line_edit = self._list_method.itemWidget(item)
            if line_edit and line_edit.text().startswith(old_method_name):
          
                parts = line_edit.text().split(' : ')
                if len(parts) > 1:
                   
                    line_edit.setText(f"{new_method_name}: {parts[1].strip()}")
                else:
                   
                    line_edit.setText(new_method_name)
                break    
    def add_relation(self, relation):
        """
        Adds a relation.
        """
        list = self._list_relation

        # Create field and add to list
        item = QListWidgetItem()
        list.addItem(item)  # !!!
        text = QLineEdit()
        text.setText(relation)
        text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Pass the QLineEdit instance 
        text.customContextMenuRequested.connect(lambda pos: self.show_row_menu(pos, text))

        # lambda ensures text is only evaluated on enter
        text.returnPressed.connect(lambda: self.verify_input(text.text(), list))

        # Formatting / Style
        list.setItemWidget(item, text)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text.setReadOnly(True)

    def remove_relation(self, relation_to_remove):
        """
        Removes a relation based on the provided relation string.
        """
        list_widget = self._list_relation

        for index in range(list_widget.count()):
            item_widget = list_widget.itemWidget(list_widget.item(index))
            if item_widget and item_widget.text() == relation_to_remove:
                # Take the item out of the list, which effectively removes it
                list_widget.takeItem(index)
                break  # Exit the loop after finding and removing the relation
                    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = True
            self.offset = event.position()

    def mouseMoveEvent(self, event):
        if self.moving:
            # Convert event.position() to QPoint
            newPos = event.position().toPoint()
            self.move(self.pos() + newPos - self.offset.toPoint())
            self.cardMoved.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = False
            
    def centerPos(self):
         return self.geometry().center()