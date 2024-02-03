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

    def setName(self, name: str) -> None:
        """
        Update entity name

        Args:
            name (str): New name to be set

        Raises:
            ValueError: If the name contains non-alphanumeric characters.
        """
        if not name.isalnum():
            raise ValueError("Name must contain only alphanumeric characters")
        self._name = name
    
    def addAttributes(self, attr: str) -> None:
        """
        Adds a new attribute to the '_attributes' set.

        Args:
            attr (str): The attribute name to be added. It should be an alphanumeric string.

        Raises:
            CustomExceptions.AttributeExistsError: If the attribute already exists in the set.
            ValueError: If the attribute name contains non-alphanumeric characters.
        """
        if attr in self._attributes:
            raise CustomExceptions.AttributeExistsError(attr)
        if not attr.isalnum():
            raise ValueError("Name must contain only alphanumeric characters")
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
        del self._attributes(attr)

    def renameAttribute(self, oldAttribute: str, newAttribute: str) -> None:
        """
        Renames an attribute from its old name to a new name

        Args:
            oldAttribute (str): The current name of the attribute to be renamed
            newAttribute (str): The new name for the attribute

        Raises:
            CustomExceptions.AttributeNotFoundError: If the old attribute name does not exits in the entity's attribute
            CustomExceptions.AttributeExitsError: If the new name is already used for another attribute
            ValueError: If the new attribute name contains non-alphanumeric characters.
        """
        if oldAttribute not in self._attributes:
            raise CustomExceptions.AttributeNotFoundError(oldAttribute)
        if newAttribute in self._attributes:
            raise CustomExceptions.AttributeExistsError(newAttribute)
        if not newAttribute.isalnum():
            raise ValueError("New name must contain only alphanumeric characters ")
        
        # Remove the old attribute and add the new attribute name
        self._attributes.remove(oldAttribute)
        self._attributes.add(newAttribute)