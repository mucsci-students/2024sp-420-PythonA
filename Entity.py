from CustomExceptions import CustomExceptions

class Entity:
    def __init__(self, name:str) -> None:
        """
        Initialize a new Entity instance.

        Args:
            name (str): The name of the entity.
        """
        self.setName(name)
        self._attributes = set()

    def getName(self) -> str:
        '''
        Return entity name

        # Returns:

        - (str): The name of entity
        
        '''
        return self._name

    def setName(self, name: str) -> None:
        """
        Update entity name

        Args:
            name (str): New name to be set
        """
        self._name = name
    
    def addAttribute(self, attr: str) -> None:
        """
        Adds a new attribute to the '_attributes' set.

        Args:
            attr (str): The attribute name to be added. It should be an alphanumeric string.

        Raises:
            CustomExceptions.AttributeExistsError: If the attribute already exists in the set.
        """
        if attr in self._attributes:
            raise CustomExceptions.AttributeExistsError(attr)
        self._attributes.add(attr)

    def deleteAttribute(self, attr: str) -> None:
        """
        Deletes an attribute from this entity if it exists.

        Args:
            attr (str): The name of the attribute to be deleted from the entity.

        Raises:
            CustomExceptions.AttributeNotFoundError: If the specified attribute is not found in the entity's attributes.
        """
        if attr not in self._attributes:
            raise CustomExceptions.AttributeNotFoundError(attr)
        self._attributes.remove(attr)

    def renameAttribute(self, oldAttribute: str, newAttribute: str) -> None:
        """
        Renames an attribute from its old name to a new name

        Args:
            oldAttribute (str): The current name of the attribute to be renamed
            newAttribute (str): The new name for the attribute

        Raises:
            CustomExceptions.AttributeNotFoundError: If the old attribute name does not exits in the entity's attribute
            CustomExceptions.AttributeExitsError: If the new name is already used for another attribute
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
