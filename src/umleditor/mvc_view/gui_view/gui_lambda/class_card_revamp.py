from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QLineEdit, QLabel, QListWidgetItem, QSizePolicy
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QPoint, QSize
from umleditor.mvc_model.diagram import Diagram


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
        self._list_relation = QListWidget()
        self._name = name
        self._size = 9

        self.initUI()
        self.diagram = Diagram()
        
        self.installEventFilter(self)
        self.moving = False
        self.offset = None
        
    def initUI(self):
        """
        Initializes the user interface of the ClassCard widget.
        """
        # Container for all of our individual widgets
        layout = QVBoxLayout()
        layout.setSpacing(0)

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
        
        self._list_fields.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        self._list_methods.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        self._list_methods.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  
        self._list_fields.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  

        self._list_methods.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 

    

        # Add Widgets to class card
        layout.addWidget(self._class_label)
        layout.addWidget(self._fields_label)
        layout.addWidget(self._list_fields)
        layout.addWidget(self._methods_label)
        layout.addWidget(self._list_methods)
       
        # Set styles
        self.set_styles()

        # Set the minimum width
        self.setMinimumWidth(150)

        # Set the layout
        self.setLayout(layout)
        self.updateSize()
        
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
        new_height = self._size * 10  
        self.setMinimumHeight(new_height)
        #self.adjustSize() 

        
    def sizeHint(self):
        return QSize(100, self._size * 20 + 40)
    
    def set_styles(self):
        """
        Sets styles for the widgets.
        """
        # Set border style for list widgets
        self._list_fields.setStyleSheet("border: 1px solid black; border-top: none")
        # Set style for class label
        self._class_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._class_label.setMinimumHeight(20)
        self._fields_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._fields_label.setMinimumHeight(15)
        self._methods_label.setStyleSheet("background-color: #6495ED; border: 1px solid black;")
        self._methods_label.setMinimumHeight(15)
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
            """
            Adds a field.
            """
            list = self._list_methods

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
            self._size += 1
            self.updateSize()
            
    def remove_method(self, field):
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
            
    def rename_method(self, old_method_name, new_method_name):
        """
        Renames an existing field in the class card.

        Args:
            old_method_name (str): The current name of the field to be renamed.
            new_method_name (str): The new name for the field.
        """
        for i in range(self._list_methods.count()):
            item = self._list_methods.item(i)
            line_edit = self._list_methods.itemWidget(item)
            if line_edit and line_edit.text().startswith(old_method_name):
                parts = line_edit.text().split(' : ')
                if len(parts) > 1:
                    
                    line_edit.setText(f"{new_method_name}: {parts[1].strip()}")
                else:
                    
                    line_edit.setText(new_method_name)
                break  

                                        
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
     
    def add_relation(self, relation):
        """
        Adds a relation.
        """
        list = self._list_relation

        # Create field and add to list
        item = QListWidgetItem()
        list.addItem(item)  
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
       