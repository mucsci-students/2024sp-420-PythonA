from Input import Input
from Output import Output
from Serializer import Serializer
from CustomExceptions import CustomExceptions as CE
from Diagram import Diagram

class Controller:
    def __init__(self) -> None:
        self._input = Input()
        self._output = Output()
        self._shouldQuit = False
        self._serializer = Serializer()
        self._diagram = Diagram()

    def run(self) -> None:
        while not self._shouldQuit:
            s = self._input.readLine()
            input = self.parse(s)
            if not (isinstance(input[0], Exception)):
                command = input[0]
                args = input[1:]
                input[0](self._diagram, *args)

            if s == 'quit' or s == 'exit':
                self._shouldQuit = True
            self._output.write('Last cmd: {}'.format(s))
        
    def save(self, path: str) -> bool:
        '''
        Saves the current diagram using a serializer to the specified file path.

        # Parameters:
        - `path` (str): The path where the diagram should be saved.

        # Returns:
        - (bool): True if the save operation is successful, False otherwise.
        '''
        return self._serializer.serialize(diagram=self._diagram, path=path)

    def load(self, path: str) -> bool:
        '''
        Loads a diagram from the specified file path using a deserializer.

        # Parameters:
        - `path` (str): The path from which the diagram should be loaded.

        # Returns:
        - (bool): True if the load operation is successful, False otherwise.
        '''
        loadedDiagram = Diagram()
        if not self._serializer.deserialize(diagram=loadedDiagram, path=path):
            return False
        self._diagram = loadedDiagram
        return True
    
    def parse (self, input:str) -> list:
        '''Parses a line of user input.
        
            Args:
                input(str) - the line to be parsed
            
            Return:
                With proper input: a list in the form [function, arg1,...,argN]
                With invalid name: CustomExceptions.InvalidArgumentError
                With invalid flag: CustomExceptions.InvalidFlagError
                With invalid command: CustomExceptions.CommandNotFoundError
        '''

        components = input.split()
        args = components[2:]

        if   len(components) < 1:
            out = [None]
        elif len(components) == 1:
            try:
                out = [self.__findFunction(command=components[0], flags=[], args=[])]
            except IndexError as e:
                out = [CE.CommandNotFoundError(components[0])]
        else:
            out = [self.__checkArgs(args)]
            if not isinstance(out[0], Exception):
                out = [self.__findFunction(command=components[0], flags=components[1], args=args)]
        return out + args

    def __checkArgs(self, args:list):
        '''Given a list of args, checks to make sure each one is valid. 
            Valid is defined as alphanumeric.
            
            Args: 
                args(list): a list of strings to be checked
            
            Raises: 
                CustomExceptions.InvalidArgumentError: at least one argument is not valid.
                
            Return: None if all args are valid
        '''
        for arg in args:
            if not(arg.isalnum()):
                return CE.InvalidArgumentError(arg)
        return None

    def __findFunction(self, command:str, flags:str, args:list):
        '''Given a command and flags, finds and returns the appropriate function
            
            Args: 
                command(str): the command to be used (ex: class)
                flags(str): the block after the command, begins with a hyphen
                
            Return: 
                With proper input: a function object that should be called
                With an invalid command: CustomExceptions.CommandNotFoundError
                With an invalid flag: CustomExceptions.InvalidFlagError
        '''
        cmd = CE.CommandNotFoundError(command)
        
        args = list(flags.strip("-")) 
        flag = args[0]  #renamed for readability

        if "class" == command:
            if   flag == "a":
                cmd = self._diagram.addEntity
            elif flag == "d":
                cmd = self._diagram.deleteEntity
            elif flag == "r":
                cmd = self.diagram.renameEntity
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "list" == command:
            if   flag == "a":
                cmd = None #TODO - List all classes and their attributes and relationships
            elif flag == "c":
                cmd = self._diagram.listEntities
            elif flag == "r":
                cmd = None #TODO - List all relationships
            elif flag == "c" and len(args) > 1: #check if they put in a class name 
                cmd = None #TODO - List all data about a given class
            else:
                cmd = CE.InvalidFlagError(flag, command)
        
        elif "save" == command:
            if   flag == "n":
                cmd = None #TODO - the command for saving a file with a name
            elif flag == "":
                cmd = None #TODO - the command to save a file based on the name of the current file
            else:
                cmd = CE.InvalidFlagError(flag, command)
        elif "load" == command:  #placeholder for eventual load flags - could be removed
            if   flag == "f":
                cmd = None #TODO - the method to load the file
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "att" == command: 
            if  flag == "a":
                cmd = None #TODO: Command that creates an attribute
            elif flag == "d":
                cmd = None #TODO: Command that deletes an attribute
            elif flag == "r":
                cmd = None #TODO: Command that renames an attribute
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "rel" == command:
            if  flag == "a":
                cmd = None #TODO: Command that adds a relationship
            elif flag == "d":
                cmd = None #TODO: Command that deletes a relationship
            else:
                cmd = CE.InvalidFlagError(flag, command)
        
        elif "exit" or "quit" == command:
            if flag == "":
                cmd = None #TODO: Quit Command
            else:
                cmd = CE.InvalidFlagError(flag, command)
        return cmd
