from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QLabel, QPushButton, QListWidget, QListWidgetItem)
class RelationWidget(QWidget):
    def __init__(self, relation="", parent=None):
        super().__init__(parent)
        self.initUI(relation)

    def initUI(self, relation):
        layout = QHBoxLayout(self)
        self.relation_edit = QLineEdit(relation)
        layout.addWidget(QLabel("Relationships:"))
        layout.addWidget(self.relation_edit)
        self.setLayout(layout)

    def get_relation(self):
        return self.relation_edit.text()
    
class FieldWidget(QWidget):
    def __init__(self, field_name="", field_type="", parent=None):
        super().__init__(parent)
        self.initUI(field_name, field_type)

    def initUI(self, field_name, field_type):
        layout = QHBoxLayout(self)
        self.field_name_edit = QLineEdit(field_name)
        self.field_type_edit = QLineEdit(field_type)
        layout.addWidget(QLabel("Field:"))
        layout.addWidget(self.field_name_edit)
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.field_type_edit)
        self.setLayout(layout)

    def get_field_info(self):
        return self.field_name_edit.text(), self.field_type_edit.text()
    
class ParamWidget(QWidget):
    def __init__(self, param="", parent=None):
        super().__init__(parent)
        self.initUI(param)

    def initUI(self, param):
        layout = QHBoxLayout(self)
        self.param_edit = QLineEdit(param)
        layout.addWidget(QLabel("Params:"))
        layout.addWidget(self.param_edit)
        self.setLayout(layout)

    def get_param(self):
        return self.param_edit.text()

class MethodWidget(QWidget):
    def __init__(self, method_name="", method_type="", params=None, parent=None):
        super().__init__(parent)
        self.initUI(method_name, method_type, params)

    def initUI(self, method_name, method_type, params):
        layout = QVBoxLayout(self)
        
        # Method name and type
        name_layout = QHBoxLayout()
        self.method_name_edit = QLineEdit(method_name)
        self.method_type_edit = QLineEdit(method_type)
        name_layout.addWidget(QLabel("Method:"))
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.method_type_edit)
        name_layout.addWidget(self.method_name_edit)
        layout.addLayout(name_layout)
        
        # Parameters list
        self.params_list_widget = QListWidget()
        if params:
            for param in params:
                self.add_param(param)
        layout.addWidget(self.params_list_widget)

        self.setLayout(layout)

    def add_param(self, param=""):
        param_widget = ParamWidget(param)
        item = QListWidgetItem(self.params_list_widget)
        item.setSizeHint(param_widget.sizeHint())
        self.params_list_widget.addItem(item)
        self.params_list_widget.setItemWidget(item, param_widget)

    def update_method_name(self, new_method_name):
        self.method_name_edit.setText(new_method_name)
        
    def get_method_info(self):
        method_name = self.method_name_edit.text()
        method_type = self.method_type_edit.text()
        params = [self.params_list_widget.itemWidget(self.params_list_widget.item(i)).get_param()
                  for i in range(self.params_list_widget.count())]
        return method_name, method_type, params

class ClassCard(QWidget):
    def __init__(self, class_name="", fields=None, methods=None, relationships=None, parent=None):
        super().__init__(parent)
        self.initUI(class_name, fields, methods, relationships)
        self._name = class_name

    def initUI(self, class_name, fields, methods, relationships):
        layout = QVBoxLayout(self)
        self.class_name_edit = QLineEdit(class_name)
        layout.addWidget(QLabel(class_name))
        layout.addWidget(self.class_name_edit)

        # Fields section
        layout.addWidget(QLabel("Fields:"))
        self.fields_list_widget = QListWidget()
        if fields:
            for field_name, field_type in fields:
                self.add_field(field_name, field_type)
        layout.addWidget(self.fields_list_widget)

        # Methods section
        layout.addWidget(QLabel("Methods:"))
        self.methods_list_widget = QListWidget()
        if methods:
            for method_name, method_type, params in methods:
                self.add_method(method_name, method_type, params)
        layout.addWidget(self.methods_list_widget)

        # Relationships section
        layout.addWidget(QLabel("Relationships:"))
        self.relationships_list_widget = QListWidget()
        if relationships:
            for rel in relationships:
                self.add_relationship(rel)
        layout.addWidget(self.relationships_list_widget)

        self.setLayout(layout)
        
    def set_name(self, new_name):
        self._name = new_name
        self.class_name.setText(new_name) 

    def add_field(self, field_name, field_type):
        field_widget = FieldWidget(field_name, field_type) 
        item = QListWidgetItem(self.fields_list_widget) 
        item.setSizeHint(field_widget.sizeHint())
        self.fields_list_widget.addItem(item)
        self.fields_list_widget.setItemWidget(item, field_widget)
    
    def remove_field(self, field_name):
        # Assuming you have a QListWidget for fields: fields_list_widget
        for index in range(self.fields_list_widget.count()):
            item = self.fields_list_widget.item(index)
            field_widget = self.fields_list_widget.itemWidget(item)
            
            if field_widget.get_name() == field_name:
                self.fields_list_widget.takeItem(index)  
                break  #
    def rename_field(self, old_field_name, new_field_name):
            # Loop through all field widgets to find the one that matches the old field name
            for index in range(self.fields_list_widget.count()):
                item = self.fields_list_widget.item(index)
                field_widget = self.fields_list_widget.itemWidget(item)
                # Assume FieldWidget has get_name and set_name methods to interact with the field's name
                if field_widget.get_name() == old_field_name:
                    field_widget.set_name(new_field_name)  # Update the field widget with the new name
                    break  # Exit the loop once the field is found and renamed                 
            
    def add_method(self, method_name="", method_type="", params=None):
        # This function creates a MethodWidget and adds it to the class card's method list
        method_widget = MethodWidget(method_name, method_type, params)
        item = QListWidgetItem(self.methods_list_widget)
        item.setSizeHint(method_widget.sizeHint())
        self.methods_list_widget.addItem(item)
        self.methods_list_widget.setItemWidget(item, method_widget)
        
    def remove_method(self, method_name, method_type=None):
        for i in range(self.methods_list_widget.count()):
            item = self.methods_list_widget.item(i)
            method_widget = self.methods_list_widget.itemWidget(item)
            current_method_name, current_method_type, _ = method_widget.get_method_info()
            
            if current_method_name == method_name and (method_type is None or current_method_type == method_type):
                self.methods_list_widget.takeItem(i)
                break        
            
    def rename_method(self, old_method_name, new_method_name, method_type=None):
        for i in range(self.methods_list_widget.count()):
            item = self.methods_list_widget.item(i)
            method_widget = self.methods_list_widget.itemWidget(item)
            current_method_name, current_method_type, _ = method_widget.get_method_info()
            
            # Check if name and type (if provided) match
            if current_method_name == old_method_name and (method_type is None or current_method_type == method_type):
                # Update the method name within the MethodWidget
                method_widget.update_method_name(new_method_name)
                break 
            
    
                    
    # def add_relationship(self, rel):
    #     # Similar structure to add_method
    #     # ...
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = True
            self.offset = event.position()

    def mouseMoveEvent(self, event):
        if self.moving:
            # Convert event.position() to QPoint
            newPos = event.position().toPoint()
            self.move(self.pos() + newPos - self.offset.toPoint())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.moving = False