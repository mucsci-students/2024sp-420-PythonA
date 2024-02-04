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
            super().__init__(f"Entity with name '{name}' does not exist.")
    
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
        Exception raised when an input argument is not valid.

        Args:
            flag (str): The name of the argument that was not found.
            command (str): The name of the command that was called with the invalid flag.
        """
        def __init__(self, flag, command) -> None:
            super().__init__(f"Command '{command}' has no flag '-{flag}'.")