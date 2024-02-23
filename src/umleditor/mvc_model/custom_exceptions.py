import re   #for argc errors
class CustomExceptions:
    class Error(Exception):
        """Base class for other exceptions."""
        pass

    #===============================================================================#
                                #Entity Exceptions
    #===============================================================================#
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
    
    #===============================================================================#
                                #Field Exceptions
    #===============================================================================#
    class FieldExistsError(Error):
        """Exception raised when a field with a given name already exists.

        Args:
            field_name (str): The name of the existing field.
        """
        def __init__(self, field_name):
            super().__init__(f"Field with name '{field_name}' already exists.")
    
    class FieldNotFoundError(Error):
        """Exception raised when a field with a given name is not found.

        Args:
            field_name (str): The name of the field not found.
        """
        def __init__(self, field_name):
            super().__init__(f"Field with name '{field_name}' does not exist.")
                        
    #===============================================================================#
                                #Relation Exceptions
    #===============================================================================#
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

    class InvalidRelationTypeError(Error):
        """
        Exception raised when the relation being added has no types.
        
        Args:
            source (Entity): The source of the relation that was being added.
            destination (Entity): The destination of the relation that was
                being added.

        """
        def __init__(self, source, destination):
            super().__init__(f"Relation between '{source} -> {destination}' has invalid type.")

    class InvalidRelationNewTypeError(Error):
        """
        Exception raised when the relation being added has invalid new type.
        
        Args:
            source (Entity): The source of the relation that was being added.
            destination (Entity): The destination of the relation that was
                being added.

        """
        def __init__(self, source, destination):
            super().__init__(f"Relation between '{source} -> {destination}' has invalid new type.")

    #===============================================================================#
                                #Method Exceptions
    #===============================================================================#
    class MethodExistsError(Error):
        """
        Exception raised when the method already exists.

        Args:
            method_name (str): The name of the method that exists.
        """
        def __init__(self, method_name):
            super().__init__(f"Method named: '{method_name}' already exists.")

    class MethodNotFoundError(Error):
        """
        Exception raised when the method was not found.

        Args:
            method_name (str): The name of the method that does not exist.
        """
        def __init__(self, method_name):
            super().__init__(f"Method named: '{method_name}' does not exist.")

    #===============================================================================#
                                #Parameter Exceptions
    #===============================================================================#
    class ParameterExistsError(Error):
        """
        Exception raised when the parameter already exists.

        Args:
            parameter_name (str): The name of the parameter that exists.
        """
        def __init__(self, parameter_name):
            super().__init__(f"Parameter named: '{parameter_name}' already exists.")

    class ParameterNotFoundError(Error):
        """
        Exception raised when the parameter was not found.

        Args:
            parameter_name (str): The name of the parameter that does not exist.
        """
        def __init__(self, parameter_name):
            super().__init__(f"Parameter named: '{parameter_name}' does not exist.")

    #===============================================================================#
                                #Parser/Controller Exceptions
    #===============================================================================#
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
    
    class InvalidArgCountError(Error):
        '''
            Exception raised when a user enters too many or too few arguments to the command they want to call.
        
            NOTE: This method really just catches the TypeError python generates and makes the message mroe readable.
            
            Args:
                error - the TypeError that needs to be replaced
        '''
        def __init__(self, error):
            #matching the different syntaxes of TypeErrors
            match = re.search(r".*(\d+).*(\d+).*", str(error))
            if match == None:
                match = re.search(r".*(\d+).*", str(error))
                super().__init__(f"{match.group(1)} too few arguments given.")
            else:
                super().__init__(f"Expected {match.group(1)} arguments, but {match.group(2)} were given.")
    
    class NoArgsGivenError(Error):
        '''
            Exception raised when a user gives no args to a command that requires one to be parsed
        '''
        def __init__(self):
            super().__init__(f"This command requires additional input. Type 'help' for command usage.")

    class NoInputError(Error):
        '''
            Exception raised when no input is given and enter is hit
        '''
        def __init__(self):
            super().__init__(f"")

    class NeedsMoreInput(Error):
        '''
            Exception raised when user gives only a command name
        '''
        def __init__(self):
            super().__init__(f"This command requires more input. Please try again or type 'help' for command usage.")
    #===============================================================================#
                                #I/O Exceptions
    #===============================================================================#

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