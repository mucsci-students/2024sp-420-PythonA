from .custom_exceptions import CustomExceptions

class Entity:
    def __init__(self, entity_name:str=''):
        """
        Constructs a new Entity object.

        Args:
            entity_name (str): The name of the entity.
        """
        self.set_name(entity_name)
        self._fields = [str]
        self._methods = [UML_Method]

    def get_name(self):
        '''
        Returns the name of the entity.

        # Returns:
            (str): The name of the entity
        '''
        return self._name

    def set_name(self, entity_name: str):
        """
        Update entity name.

        Args:
            entity_name (str): The new name for the entity.
        """
        self._name = entity_name
    
    def add_field(self, field_name:str):
        """
        Adds a new field to the to the list.

        Args:
            field_name (str): The field' name to be added to the entity.

        Raises:
            CustomExceptions.FieldExistsError: If the field already
                exists in the Entity.
        """
        if field_name in self._fields:
            raise CustomExceptions.FieldExistsError(field_name)
        else:
            self._fields.append(field_name)

    def delete_field(self, field_name: str):
        """
        Deletes a field from this entity if the field exists.

        Args:
            field_name (str): The name of the field to be deleted from the entity.

        Raises:
            CustomExceptions.FieldNotFoundError: If the specified field
                is not found in the entity's field list.
        """
        if field_name not in self._fields:
            raise CustomExceptions.FieldNotFoundError(field_name)
        else:
            self._fields.remove(field_name)

    def rename_field(self, old_field: str, new_field: str):
        """
        Renames a field from its old name to a new name

        Args:
            old_field(str): The current name of the field.
            new_field (str): The new name for the field.

        Raises:
            CustomExceptions.FieldNotFoundError: If the old field does 
                not exist in the entity.
            CustomExceptions.FieldExistsError: If the new name is already 
                used for another field in this entity.
        """
        if old_field not in self._fields:
            raise CustomExceptions.FieldNotFoundError(old_field)
        
        elif new_field in self._fields:
            raise CustomExceptions.FieldExistsError(new_field)
        else:
            self._fields.remove(old_field)
            self._fields.append(new_field)

    def add_method(self, method_name: str):
        if any(method_name == um.get_name() for um in self._methods):
            raise CustomExceptions.MethodExistsError(method_name)
        else:
            new_method = UML_Method(method_name)
            self._methods.append(new_method)

    def delete_method(self, method_name: str):
        for um in self._methods:
            if um.get_name == method_name:
                self._methods.remove(um)
            else:
                raise CustomExceptions.MethodNotFoundError(method_name)

    def rename_method(self, old_name: str, new_name: str):
        if not any(old_name == um.get_name() for um in self._methods):
            raise CustomExceptions.MethodNotFoundError(old_name)
        elif any(new_name == um.get_name() for um in self._methods):
            raise CustomExceptions.MethodExistsError(new_name)
        else:
            for um in self._methods:
                if (old_name == um.get_name()):
                    self._methods.remove(um)
            new_method = UML_Method(new_name)
            self._methods.append(new_method)

    def __str__(self) -> str:
        """
        Returns the string representation of the Entity object (its name).

        Returns:
            str: The name of the entity.
        """
        return self._name

class UML_Method:
    def __init__(self, method_name):
        self._name = method_name
        self._params = []

    def get_name(self):
        return self._name
    
    def set_name(self, new_name):
        self._name = new_name