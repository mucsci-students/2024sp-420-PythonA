import Input
import Output
import Serializer
from CustomExceptions import CustomExceptions as CE
from Diagram import Diagram
import os
import Help

class Controller:
    def __init__(self) -> None:
        self._shouldQuit = False
        self._diagram = Diagram()

        self._command_flag_map = {
            "class" : ["a","d","r"],
            "list"  : ["a","c","r","d"],
            "save"  : [],
            "load"  : [],
            "att"   : ["a","d","r"],
            "rel"   : ["a","d"],
            "exit"  : [],
            "quit"  : [],
            "help"  : []
        }

        self._functions = [
            "add_entity",
            "delete_entity",
            "rename_entity",
            "list_everything",
            "list_entities",
            "list_relations",
            "list_entity_details",
            "save",
            "load",
            "add_attribute",
            "delete_attribute",
            "rename_attribute",
            "add_relation",
            "delete_relation",
            "quit",
            "help"
        ]
    def run(self) -> None:
        while not self._shouldQuit:
            s = Input.readLine()
            input = self.parse(s)

            if not isinstance(input[0], Exception) and input != None:
                command = input[0]
                args = input[1:]
                out = ""
                try:
                    out = command(*args)
                except Exception as e:
                    Output.write(str(e))

                if out != None:
                    Output.write(str(out))  
            else:
                Output.write(str(input[0]))
            
    def quit(self):
        '''Basic Quit Routine. Prompts user to save, where to save, 
            validates input.
            
        Returns:
            If the name and filepath were valid or user doesn't want to save, returns true
            If name is invalid, returns invalid filename exception
            If filepath is invalid, returns invalid filepath exception
        '''
        self._shouldQuit = True
        while True:
            answer = Input.readLine('Would you like to save before quit? [Y]/n: ').strip()
            if not answer or answer in ['Y', 'n']: # default or Y/n
                break
        if answer == 'n':
            #user wants to quit without saving
            return
        else:
            answer = Input.readLine('Name of file to save: ')

        if isinstance(self.__checkArgs([answer]), Exception):
            return CE.IOFailedError("Save", "invalid filename")

        if self.save(answer):
            return
        return CE.IOFailedError("Save", "an unknown fatal error")

    def save(self, name: str) -> bool:
        '''
        Saves the current diagram using a serializer with the given filename

        #### Parameters:
        - `name` (str): The name of the file to be saved.

        #### Returns:
        - (bool): True if the save operation is successful, False otherwise.
        '''
        path = os.path.join(os.path.dirname(__file__), 'save')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name + '.json')
        return Serializer.serialize(diagram=self._diagram, path=path)

    def load(self, name: str) -> bool:
        '''
        Loads a diagram with the given filename using a deserializer.

        #### Parameters:
        - `path` (str): The name of the file to be loaded.

        #### Returns:
        - (bool): True if the load operation is successful, False otherwise.
        '''
        path = os.path.join(os.path.dirname(__file__), 'save')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name + '.json')
        loadedDiagram = Diagram()
        if not Serializer.deserialize(diagram=loadedDiagram, path=path):
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
            out = self.__findFunction("")
        elif len(components) == 1:
            out = self.__findFunction(command=components[0])
        #this case only exists for help. It could be removed but the syntax of help would feel weird.
        elif len(components) == 2:
            out = self.__findFunction(command=components[0], flags=components[1])
            
            if not components[1].__contains__("-"):
                args = components[1:]
        else:
            out = self.__checkArgs(args)
            if not isinstance(out, Exception):
                out = self.__findFunction(command=components[0], flags=components[1], args=args)
            
        return [out] + args

    def __checkArgs(self, args:list):
        '''Given a list of args, checks to make sure each one is valid. 
            Valid is defined as alphanumeric.
            
            Args: 
                args(list): a list of strings to be checked
                
            Return: 
                CustomExceptions.InvalidArgumentError if an argument provided is invalid
                The list of args provided if all args are valid
        '''
        for arg in args:
            if not(arg.isalnum()):
                return CE.InvalidArgumentError(arg)
        return args


        
    def __findFunction(self, command:str, flags:str = "", args:list = []):
        '''Given a command and flags, finds and returns the appropriate function
            
            Args: 
                command(str): the command to be used (ex: class)
                flags(str): the block after the command, begins with a hyphen
                
            Return: 
                With proper input: a function object that should be called
                With an invalid command: CustomExceptions.CommandNotFoundError
                With an invalid flag: CustomExceptions.InvalidFlagError
        '''
        while (True):
            input_str = input("Call by name with args [ex: 'first_method eval gt 21], CTRL-C to quit: ")
            parts = input_str.split()   #splitting string into list
            method_name = parts[0]      #first element in list (python indexes are 0-based!)
            args = parts[1:]            #rest of elements -- https://realpython.com/lessons/string-slicing/

            if hasattr(obj, method_name):               #we can check an object for a member by name, or combine args to generate names!
                method = getattr(obj, method_name)      #we can grab an actual object - like a member function - by a name
                method(*args)                           #we can call it, and pass in our args. https://hyperskill.org/learn/step/15401
            else:
                print("Method not found.")