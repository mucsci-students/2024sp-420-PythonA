from CustomExceptions import CustomExceptions

class Entity:
    def __init__(self, name:str) -> None:
        """
        Constructs a new Entity object.

        Args:
            name (str): The name of the entity.
        """
        self.set_name(name)
        self._attributes = set()

    def get_name(self) -> str:
        '''
        Returns the name of the entity.

        # Returns:
            (str): The name of the entity
        '''
        return self._name

    def set_name(self, name: str) -> None:
        """
        Update entity name.

        Args:
            name (str): The new name for the entity.
        """
        self._name = name
    
    def add_attribute(self, attr:str) -> None:
        """
        Adds a new attribute to the to the entity.

        Args:
            attr (str): The attribute name to be added to the entity.

        Raises:
            CustomExceptions.AttributeExistsError: If the attribute already
                exists in the Entity.
        """
        if attr in self._attributes:
            raise CustomExceptions.AttributeExistsError(attr)
        self._attributes.add(attr)

    def delete_attribute(self, attr: str) -> None:
        """
        Deletes an attribute from this entity if it exists.

        Args:
            attr (str): The name of the attribute to be deleted from the entity.

        Raises:
            CustomExceptions.AttributeNotFoundError: If the specified attribute
                is not found in the entity's attributes.
        """
        if attr not in self._attributes:
            raise CustomExceptions.AttributeNotFoundError(attr)
        self._attributes.remove(attr)

    def rename_attribute(self, oldAttribute: str, newAttribute: str) -> None:
        """
        Renames an attribute from its old name to a new name

        Args:
            oldAttribute (str): The current name of the attribute.
            newAttribute (str): The new name for the attribute

        Raises:
            CustomExceptions.AttributeNotFoundError: If the old attribute does 
                not exist in the entity.
            CustomExceptions.AttributeExistsError: If the new name is already 
                used for another attribute in this entity.
        """
        if oldAttribute not in self._attributes:
            raise CustomExceptions.AttributeNotFoundError(oldAttribute)
        
        if newAttribute in self._attributes:
            raise CustomExceptions.AttributeExistsError(newAttribute)
        # Remove the old attribute and add the new attribute name
        self._attributes.remove(oldAttribute)
        self._attributes.add(newAttribute)

    def __str__(self) -> str:
        """
        Returns the string representation of the Entity object (its name).

        Returns:
            str: The name of the entity.
        """
        return self._name
