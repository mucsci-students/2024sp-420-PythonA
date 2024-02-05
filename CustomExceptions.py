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
                        
    class RelationExistsError(Error):
        """
        Exception raised when the relation being added already exists.
        
        Args:
            source (Entity): The source of the relation that was being added.
            destination (Entity): The destination of the relation that was
                being added.
                
        """
        def __init__(self, source, destination):
            super().__init__(f"Relation between '{source} -> {destination}' already exists.")
            
    class RelationDoesNotExistError(Error):
        """
        Exception raised when the relation being deleted does not exist.
        
        Args:
            source (Entity): The source of the relation that was being deleted.
            destination (Entity): The destination of the relation that was
                being deleted.

        """
        def __init__(self, source, destination):
            super().__init__(f"Relation between '{source} -> {destination}' does not exist.")
    
    class InvalidArgumentError(Error):
        """
        Exception raised when an input argument is not valid.

        Args:
            name (str): The name of the argument that was not found.
        """
        def __init__(self, name) -> None:
            super().__init__(f"Argument '{name}' is not alphanumeric.")
    
    class InvalidFlagError(Error):
        """
        Exception raised when an input flag is not valid.

        Args:
            flag (str): The name of the flag that was not found.
            command (str): The name of the command that was called with the invalid flag.
        """
        def __init__(self, flag, command) -> None:
            super().__init__(f"Command '{command}' has no flag '-{flag}'.")

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