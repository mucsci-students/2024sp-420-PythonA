class CustomExceptions:
    class Error(Exception):
        """Base class for other exceptions."""
        pass

    class EntityExistsError(Error):
        """Exception raised when an entity with a given name already exists.

        Args:
            name (str): The name of the existing entity.
        """
        def __init__(self, name) -> None:

            super().__init__(f"Object with name '{name}' already exists.")
    
    class CommandNotFoundError(Error):
        """Exception raised when an invalid command is entered"""

        def __init__(self, name) -> None:
            super().__init__(f"Command '{name}' does not exist. Try again or type 'help' for help.")

    class EntityNotFoundError(Error):
        """
        Exception raised when an entity with the given name is not found.

        Args:
            name (str): The name of the entity not found.
        """
        def __init__(self, name) -> None:
            super().__init__(f"Entity with name '{name}' does not exists.")

    class AttributeExistsError(Error):
        """Exception raised when an attribute with a given name already exists.

        Args:
            attr (str): The name of the existing attribute.
        """
        def __init__(self, attr) -> None:
            super().__init__(f"Attribute with name '{attr}' already exists.")
    
    class AttributeNotFoundError(Error):
        """Exception raised when an attribute with a given name is not found.

        Args:
            attr (str): The name of the attribute not found.
        """
        def __init__(self, attr) -> None:
            super().__init__(f"Attribute with name '{attr}' does not exist.")
