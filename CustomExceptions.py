class CustomExceptions:
    class Error(Exception):
        """Base class for other exceptions."""
        pass

    #===============================================================================
                                #Entity Exceptions
    #===============================================================================
    class EntityExistsError(Error):
        """Exception raised when an entity with a given name already exists.

        Args:
            name (str): The name of the existing entity.
        """
        def __init__(self, name) -> None:
            super().__init__(f"Entity with name '{name}' already exists.")

    class EntityNotFoundError(Error):
        """
        Exception raised when an entity with the given name is not found.

        Args:
            name (str): The name of the entity not found.
        """
        def __init__(self, name) -> None:
            super().__init__(f"Entity with name '{name}' does not exist.")
    
    #===============================================================================
                                #Attribute Exceptions
    #===============================================================================
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
                        
    #===============================================================================
                                #Relation Exceptions
    #===============================================================================
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

    #===============================================================================
                                #Parser/Controller Exceptions
    #===============================================================================
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
            super().__init__(f"Command '{command}' has no flag '{flag}'.")
    
    class NoEntitySelected(Error):
        """
        Exception raised when an input argument is not valid.

        Args:
            flag (str): The name of the argument that was not found.
            command (str): The name of the command that was called with the invalid flag.
        """
        def __init__(self) -> None:
            super().__init__(f"No class selected. Use 'class -s name' to select a class.")

    class CommandNotFoundError(Error):
        """Exception raised when an invalid command is entered"""

        def __init__(self, name) -> None:
            super().__init__(f"Command '{name}' does not exist. Try again or type 'help' for help.")
    
    #===============================================================================
                                #I/O Exceptions
    #===============================================================================

    class IOFailedError(Error):
        '''Exception raised when an I/O Operation fails (saving or loading)
        
        Args:
            opname (str): the name of the operation that failed
            reason (str): the reason that opname failed
        '''
        def __init__(self, opname, reason) -> None:
            super().__init__(f"{opname} failed due to {reason}. Please try again.")

    class ReadFileError(Error):
        '''Exception raised when failed to read a file
        
        #### Args:
            `filepath` (str): the path of the file to read
        '''
        def __init__(self, filepath: str) -> None:
            super().__init__('Can not read file: "{}".'.format(filepath))

    class WriteFileError(Error):
        '''Exception raised when failed to write a file
        
        #### Args:
            `filepath` (str): the path of the file to write
        '''
        def __init__(self, filepath: str) -> None:
            super().__init__('Can not write file: "{}".'.format(filepath))

    #===============================================================================
                                #Serializer Exceptions
    #===============================================================================
            
    class JsonDecodeError(Error):
        '''Exception raised when failed to decode a Json file
        
        #### Args:
            `filepath` (str): the path of the Json file to decode
        '''
        def __init__(self, filepath: str) -> None:
            super().__init__('Can not decode .json file: "{}".'.format(filepath))
    
    class JsonEncodeError(Error):
        '''Exception raised when failed to encode a Json file
        
        #### Args:
            `filepath` (str): the path of the Json file to encode
        '''
        def __init__(self, filepath: str) -> None:
            super().__init__('Can not encode .json file: "{}".'.format(filepath))

    class SavedDataError(Error):
        '''Exception raised when the saved data is not consistent with the Diagram.
        
        #### Args:
            `filepath` (str): the path of the save file
        '''
        def __init__(self, filepath: str) -> None:
            fmt = 'Failed to load save data: "{}".(Data in this save is no longer valid)'
            super().__init__(fmt.format(filepath))