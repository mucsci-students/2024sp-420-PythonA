from Input import Input
from Output import Output
from Serializer import Serializer
from CustomExceptions import CustomExceptions as CE
from Diagram import Diagram
import os
from Help import basicHelp, cmdHelp

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
                func = command(*args)
                self._output.write(str(func))
            else:
                self._output.write(str(input[0]))
            
            #quit routine entrypoint TODO: Move to __findFunction
            if s == 'quit' or s == 'exit':
                exit_prep = self.quit()
                if(exit_prep == True):
                    self._shouldQuit = True
                else:
                    self._output.write(str(exit_prep))
                    
    def quit(self):
        '''Basic Quit Routine. Prompts user to save, where to save, 
            validates input.
            
        Returns:
            If the name and filepath were valid or user doesn't want to save, returns true
            If name is invalid, returns invalid filename exception
            If filepath is invalid, returns invalid filepath exception
        '''
        self._output.write("Would you like to save? [y]/n: ")
        answer = self._input.readLine("")
        if answer != "n" or "N" or "no" or "No":
            self._output.write("Name of file to save: ")
            answer = self._input.readLine("")
        else:
            #user wants to quit without saving
            return True
        
        if self.__checkArgs([answer]) == None:
            self._output.write("Filepath to save to: ")
            fp = self._input.readLine("")
        else:
            return CE.IOFailedError("Save", "invalid filename")
        fp += answer + '.json'
        if os.path.exists(fp):
            self._serializer.serialize(self._diagram, fp)
            return True
        else:
            return CE.IOFailedError("Save", "invalid filepath")
        return CE.IOFailedError("Save", "an unknown fatal error")

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
        
        args = list(flags)
        print("args: ", args)
        flag = args[1] #renamed for readability
        print("flag: ", flag)
        if "class" == command:
            if   flag == "a":
                cmd = self._diagram.addEntity
            elif flag == "d":
                cmd = self._diagram.deleteEntity
            elif flag == "r":
                cmd = self._diagram.renameEntity
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
            cmd = Serializer.serialize

        elif "load" == command: 
            cmd = Serializer.deserialize

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
                cmd = self._diagram.add_relation
            elif flag == "d":
                cmd = self._diagram.delete_relation
            else:
                cmd = CE.InvalidFlagError(flag, command)
        #TODO: how to handle commands with no flags sometimes?
        elif "exit" or "quit" == command:
            if flag == None:
                cmd = None #TODO: Quit Command
            else:
                cmd = CE.InvalidFlagError(flag, command)
        elif "help" == command:
            #TODO - implement all the specific help calls
            if len(args) == 0:
                cmd = basicHelp
            else:
                cmd = CE.InvalidFlagError(flag, command)
        return cmd
