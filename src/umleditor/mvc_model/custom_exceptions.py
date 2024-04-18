# Primary: Danish
# Secondary: Zhang


import re   #for argc errors
class CustomExceptions:
    class Error(Exception):
        """Base class for other exceptions."""
        pass

    # ===============================================================================#
                             # Redo State Unfounded
    # ===============================================================================#
    class RedoStateError(Error):
        """Exception raised when redo state is undefined by any prior undo actions.

        """
        def __init__(self) -> None:
            super().__init__(f"Redo state not defined!")

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
        def __init__(self, field_name: str):
            super().__init__(f"Field with name '{field_name}' already exists.")
    
    class FieldNotFoundError(Error):
        """Exception raised when a field with a given name is not found.

        Args:
            field_name (str): The name of the field not found.
        """
        def __init__(self, field_name):
            super().__init__(f"Field with name '{field_name}' does not exist.")

    class FieldtypeNotFoundError(Error):
        """Exception raised when a field with a given name is not found.

        Args:
            field_type (str): The name of the field not found.
        """

        def __init__(self, field_type:str):
            super().__init__(f"Field type '{field_type}' does not exist.")

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
            invalid_type (str): The type of the relation that was being added.

        """
        def __init__(self, invalid_type):
            super().__init__(f"{invalid_type} is not a valid relation type.")

    class SelfRelationError(Exception):
        """
        Exception raised when a relation is added between an entity and itself.

        Args: entity_name (str): The name of the entity that is trying to relate 
                                    to itself.


        """
        def __init__(self, entity_name):
            super().__init__(f"A self-relation for entity '{entity_name}' is not" 
                             f"allowed.")

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

    class DuplicateParametersError(Error):
        """
        Exception raised when the parameter occurs more than once.

        Args:
            parameter_name (str): The name of the parameter occurs more than once.
        """
        def __init__(self, parameter_name):
            super().__init__(f"Parameter named: '{parameter_name}' occurs more than once.")

    class ParameterInvalidTypeError(Error):
        """
        Exception raised when the parameter type mismatched.

        Args:
        parameter_type (str): The type of the parameter is mismatched or not allowed.
        """

        def __init__(self, parameter_type):
            super().__init__(f"Type '{parameter_type}' is not allowed.")


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
            super().__init__(f"No class selected.")

    class CommandNotFoundError(Error):
        """Exception raised when an invalid command is entered"""

        def __init__(self, name) -> None:
            super().__init__(f"Command '{name}' does not exist.")
    
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

    class NeedsMoreInput(Error):
        '''
            Exception raised when user gives only a command name
        '''
        def __init__(self):
            super().__init__(f"This command requires more input.")
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

