from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit, QLabel, QListWidgetItem
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QPoint


class ClassCard (QWidget):
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
        self._size = 9
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

        # Labels for fields and methods
        self._fields_label = QLabel("Fields:")
        self._fields_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._methods_label = QLabel("Methods:")
        self._methods_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    
        # Create list widgets
        self._list_fields = QListWidget()
        self._list_methods = QListWidget()
    

        # Add Widgets to class card
        layout.addWidget(self._class_label)
        layout.addWidget(self._fields_label)
        layout.addWidget(self._list_fields)
        layout.addWidget(self._methods_label)
        layout.addWidget(self._list_methods)
       
        # Set styles
        self.set_styles()

        # Set the minimum width
        self.setMinimumWidth(100)

        # Set the layout
        self.setLayout(layout)
        
    def set_name(self, name: str):
            """
            Sets the name of the class.

            Args:
                name (str): The name of the class.
            """
            self._name = name
            self._class_label.setText(name)
            
    def updateSize(self):
        """
        Update the size of the ClassCard dynamically based on the content.
        """

        # Calculate the new height based on the number of items
        new_height = max(self._size * 20, 200)  # Minimum height of 200, increase by 20 for each item

        # Set the new size
        self.setFixedHeight(new_height)
    
    def set_styles(self):
        """
        Sets styles for the widgets.
        """
        # Set border style for list widgets
        self._list_fields.setStyleSheet("border: 1px solid black; border-top: none")
        self._list_methods.setStyleSheet("border: 1px solid black; border-bottom: none; border-top: none;")
        # Set style for class label
        self._class_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._class_label.setMinimumHeight(30)
        self._fields_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._fields_label.setMinimumHeight(20)
        self._methods_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._methods_label.setMinimumHeight(20)
        # Set style for entire widget
        self.setStyleSheet("background-color: white;")
    def add_field(self, field):
            """
            Adds a field.
            """
            list = self._list_fields

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
            self._size += 1
            self.updateSize()
            
    def remove_field(self, field):
        """
        Removes a field from the class card.

        Args:
            field (str): The field to remove.
        """
        for i in range(self._list_fields.count()):
            item = self._list_fields.item(i)
            line_edit = self._list_fields.itemWidget(item)
            if line_edit and line_edit.text().startswith(field):
                self._list_fields.takeItem(i)
                self._size -= 1
                self.updateSize()
                break
            
    def rename_field(self, old_field_name, new_field_name):
        """
        Renames an existing field in the class card.

        Args:
            old_field_name (str): The current name of the field to be renamed.
            new_field_name (str): The new name for the field.
        """
        for i in range(self._list_fields.count()):
            item = self._list_fields.item(i)
            line_edit = self._list_fields.itemWidget(item)
            if line_edit and line_edit.text().startswith(old_field_name):
                parts = line_edit.text().split(' : ')
                if len(parts) > 1:
                    
                    line_edit.setText(f"{new_field_name}: {parts[1].strip()}")
                else:
                    
                    line_edit.setText(new_field_name)
                break    

    def add_method(self, method):
        method_widget = MethodWidget(method)
        item = QListWidgetItem(self._list_methods)  
        item.setSizeHint(method_widget.sizeHint())  
        self._list_methods.addItem(item)  
        self._list_methods.setItemWidget(item, method_widget)  
        self._size += 2
        self.updateSize()

    def remove_method(self, method_name):
        # Iterate over all items in the QListWidget
        for i in range(self._list_methods.count()):
            item = self._list_methods.item(i)
            method_widget = self._list_methods.itemWidget(item)
            if method_widget and method_widget._method_label.text() == method_name:
                self._list_methods.takeItem(i)  
                method_widget.deleteLater() 
                self._size -= 2
                self.updateSize()
                break
            
    def rename_method(self, old_method_name, new_method_name):
        for i in range(self._list_methods.count()):
            item = self._list_methods.item(i)
            method_widget = self._list_methods.itemWidget(item)
            if method_widget and method_widget._method_label.text() == old_method_name:
                method_widget.rename_method(new_method_name)
                break
        
    def add_param(self, method, param):
        for methodCard in self.findChildren(MethodWidget):
            if methodCard._method_label == method:
                methodCard.add_param(param)
            self._size += 1
            self.updateSize()
                        
        
    def remove_param(self, method, param):
        for methodCard in self.findChildren(MethodWidget):
            if methodCard._method_label == method:
                methodCard.remove_param(param)  
            self._size -= 1
            self.updateSize()
                
                
    def rename_param(self, method, old_param_name, new_param_name):
        for methodCard in self.findChildren(MethodWidget):
            if methodCard._method_label == method:
                methodCard.rename_param(old_param_name, new_param_name)  
                                        
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
     
class MethodWidget(QWidget):
    def __init__(self, method_name):
        super().__init__()
        layout = QVBoxLayout()
        self._method_label = QLabel(method_name)
        self._params_label = QLabel("Params:")
        self._list_params = QListWidget()
        
        
        layout.addWidget(self._method_label)
        layout.addWidget(self._params_label)
        layout.addWidget(self._list_params)
        
        self._list_params.setStyleSheet("border: 1px solid black; border-bottom: none; border-top: none;")
        self._params_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._params_label.setMinimumHeight(10)
        
        self.setLayout(layout) 
        
    def rename_method(self, name: str):
            """
            Sets the name of the method.

            Args:
                name (str): The name of the class.
            """
            parts = self._method_label.text().split(' : ')
            
            self._method_label.setTextf(f"{name}: {parts[1].strip()}")
           
    def add_param(self, param):
            """
            Adds a param.
            """
            list = self._list_params

            # Create param and add to list
            item = QListWidgetItem()
            list.addItem(item) 
            text = QLineEdit()
            text.setText(param)
            text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

            # Pass the QLineEdit instance 
            text.customContextMenuRequested.connect(lambda pos: self.show_row_menu(pos, text))

            # lambda ensures text is only evaluated on enter
            text.returnPressed.connect(lambda: self.verify_input(text.text(), list))

            # Formatting / Style
            list.setItemWidget(item, text)
            text.setAlignment(Qt.AlignmentFlag.AlignCenter)

            text.setReadOnly(True)
            
    def remove_param(self, param):
        """
        Removes a param from the class card.

        Args:
            param_name (str): The name of the param to remove.
        """
        for i in range(self._list_params.count()):
            item = self._list_params.item(i)
            line_edit = self._list_params.itemWidget(item)
            if line_edit and line_edit.text() == param:
                self._list_params.takeItem(i)
                break            
 
    def rename_param(self, old_param_name, new_param_name):
            """
            Renames an existing param in the class card.

            Args:
                old_param_name (str): The current name of the param to be renamed.
                new_param_name (str): The new name for the param.
            """
            for i in range(self._list_params.count()):
                item = self._list_params.item(i)
                line_edit = self._list_params.itemWidget(item)
                if line_edit and line_edit.text() == old_param_name:
                    line_edit.setText(new_param_name)
                    break               