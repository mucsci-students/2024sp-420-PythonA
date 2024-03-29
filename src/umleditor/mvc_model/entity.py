from .custom_exceptions import CustomExceptions

class Entity:
    def __init__(self, entity_name:str=''):
        """
        Constructs a new Entity object.

        Args:
            entity_name (str): The name of the entity.
        """
        self._name:str = entity_name
        self._fields: list[str] = []
        self._methods: list[UML_Method] = []

    def get_name(self):
        """
        Returns the name of the entity.

        # Returns:
            (str): The name of the entity
        """
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

        Returns:
            None.
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

        Returns:
            None.
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

        Returns:
            None.
        """
        if old_field == new_field:
            return
        if old_field not in self._fields:
            raise CustomExceptions.FieldNotFoundError(old_field)
        
        elif new_field in self._fields:
            raise CustomExceptions.FieldExistsError(new_field)
        else:
            self._fields[self._fields.index(old_field)] = new_field

    def get_method(self, method_name:str):
        """
        Checks if a method exists inside an entity.

        Args:
            method_name (str): The method's name to be checked for.

        Raises:
            None.

        Returns:
            UML_Method: Returns method if it exists
        """
        for m in self._methods:
            if m.get_method_name() == method_name:
                return m
        raise CustomExceptions.MethodNotFoundError(method_name)
        
    def add_method(self, method_name: str):
        """
        Adds a new method to the to the list.

        Args:
            method_name (str): The method's name to be added to the entity.

        Raises:
            CustomExceptions.MethodExistsError: If the method already
                exists in the Entity.
        Returns:
            None.
        """
        if any(method_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodExistsError(method_name)
        else:
            new_method = UML_Method(method_name)
            self._methods.append(new_method)
    
    def add_method_and_params(self, method_name: str, *params) :
        """
        Adds a method with specified parameters to the class.

        Parameters:
            method_name (str): The name of the method to add.
            *params: Variable-length argument list representing the parameters for the method.
        """
        self.add_method(method_name)
        self.get_method(method_name).add_parameters(list(params))

    def edit_method(self, old_method: str, new_method: str,  *params):
        deleted_method = self.get_method(old_method) 
        self.delete_method(old_method)
        try:
            self.add_method_and_params(new_method, *params)
        except Exception as e:
            self._methods.append(deleted_method)
            raise e

    def delete_method(self, method_name: str):
        """
        Deletes a method from this entity if the method exists.

        Args:
            method_name (str): The name of the method to be deleted from the entity.

        Raises:
            CustomExceptions.MethodNotFoundError: If the specified method
                is not found in the entity's method list.

        Returns:
            None.
        """
        if not any(method_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodNotFoundError(method_name)
        for um in self._methods:
            if um.get_method_name() == method_name:
                self._methods.remove(um)

    def rename_method(self, old_name: str, new_name: str):
        """
        Renames a method from its old name to a new name

        Args:
            old_name(str): The current name of the method.
            new_name (str): The new name for the method.

        Raises:
            CustomExceptions.MethodNotFoundError: If the old method does 
                not exist in the entity.
            CustomExceptions.MethodExistsError: If the new name is already 
                used for another method in this entity.

        Returns:
            None.
        """
        if not any(old_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodNotFoundError(old_name)
        elif any(new_name == um.get_method_name() for um in self._methods):
            raise CustomExceptions.MethodExistsError(new_name)
        else:
            for um in self._methods:
                if (old_name == um.get_method_name()):
                    um.set_method_name(new_name)
    
    def list_fields(self):
        '''Lists all the fields of this entity
        
            Return: a comma separated list of all methods in this entity
        '''
        return ", ".join(str(f) for f in self._fields) + '\n'
    
    def list_methods(self):
        '''Lists all the methods of this entity
        
            Return: a comma separated list of all methods and their params in this entity
        '''
        return ", ".join(m.__str__() for m in self._methods) + '\n'

    def __str__(self) -> str:
        """
        Returns the string representation of the Entity object (its name).

        Returns:
            str: The name of the entity.
        """
        return self._name
    
    def __eq__ (self, other):
        '''Equality operator for entities
            
            Return:
            True - this and other have the same name
            False - this and other do not have the same name
        '''
        return self._name == other._name

#====================================================================================#
#                                  Method Definition
#====================================================================================#
     
class UML_Method:

    def __init__(self, method_name=''):
        """
        Creates a UML_Method object.
        
        Args:
            method_name (str): The name of the method.
            
        Raises:
            None.
            
        Returns:
            None.
        """
        self._name:str = method_name
        self._params:list[str] = []

    def get_method_name(self):
        """
        Returns the name of the method.
        
        Args:
            None.
            
        Raises:
            None.
        
        Returns:
            name (Entity): The name of the method.
        """
        return self._name
    
    def set_method_name(self, new_name):
        """
        Changes the name of the method.
        
        Args:
            new_name (str): The new name of the method.
            
        Raises:
            None.
        
        Returns:
            None.
        """
        self._name = new_name

    def _check_duplicate_paramters(self, params: list[str]):
        """
        Checks if there are duplicate paramters.
        
        Args:
            params (list[str]): The list of new parameters to be checked.
            
        Raises:
            CustomExceptions.DuplicateParametersError: If any of the parameter occurs more than once.
        """
        for param in params:
            if params.count(param) != 1:
                raise CustomExceptions.DuplicateParametersError(param)

    def add_parameters(self, params: list[str]):
        """
        Adds a list of new parameters to the method.

        Args:
            params (list[str]): The list of new parameters to be added.

        Raises:
            CustomExceptions.ParameterExistsError: If any of the parameter already exists in the method.

        Returns:
            None.
        """
        self._check_duplicate_paramters(params)
        for new_param in params:
            if new_param in self._params:
                raise CustomExceptions.ParameterExistsError(new_param)
        self._params.extend(params)

    def remove_parameters(self, params: list[str]):
        """
        Removes a list of parameters from the method.

        Args:
            params (list[str]): The list of parameters to be removed.

        Raises:
            CustomExceptions.ParameterNotFoundError: If any of the parameter does not exist in the method.

        Returns:
            None.
        """
        self._check_duplicate_paramters(params)
        for remove_param in params:
            if remove_param not in self._params:
                raise CustomExceptions.ParameterNotFoundError(remove_param)
        for remove_param in params:
            self._params.remove(remove_param)

    def change_parameters(self, old_params: list[str], new_params: list[str]):
        """
        Changes a list of parameters to a new list of parameters to the method.

        Args:
            old_params (list[str]): The list of parameters to be removed.
            new_params (list[str]): The list of new parameters to be added.

        Raises:
            CustomExceptions.ParameterNotFoundError: If any of the parameter to be removed does not exist in the method.
            CustomExceptions.ParameterExistsError: If any of the parameter to be added already exists in the method.

        Returns:
            None.
        """
        self._check_duplicate_paramters(old_params)
        self._check_duplicate_paramters(new_params)
        for remove_param in old_params:
            if remove_param not in self._params:
                raise CustomExceptions.ParameterNotFoundError(remove_param)
        deleted_params = []
        for remove_param in old_params:
            idx = self._params.index(remove_param)
            deleted_params.append([idx, self._params[idx]])
            del self._params[idx]
        for new_param in new_params:
            if new_param in self._params:
                # restore all deleted parameters if add operation should fail
                for idx, deleted_param in reversed(deleted_params):
                    self._params.insert(idx, deleted_param)
                raise CustomExceptions.ParameterExistsError(new_param)
        self._params.extend(new_params)
        
    def __str__(self):
        """
        Returns the name of the method and a list of it's parameters.
        
        Args:
            None.
            
        Raises:
            None.
        
        Returns:
            name (str): A templated string to represent a method and
                its list of parameters.
        """
        result = self.get_method_name()
        result += "\n\t" + self.get_method_name() + "'s Params:\n\t\t"
        param_results = ', '.join(p for p in self._params)
        return result + param_results
    
    def __eq__ (self, o):
        """Equality operator for Methods - checks equality of both fields"""
        if self is o:
            return True
        if o is None: 
            return False
        
        if self._name != o._name:
            return False
        for param in self._params:
            if not o._params.__contains__(param):
                return False
        return True