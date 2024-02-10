import Input
import Output
import Serializer
from CustomExceptions import CustomExceptions as CE
from Diagram import Diagram
import os
import Help

#Parser Includes. These will be moved out when the parser is moved.
from Entity import Entity
from Relation import Relation




class Controller:
    def __init__(self) -> None:
        self._shouldQuit = False
        self._diagram = Diagram()

        #map relating commands to the flags that can be passed to them
        #NOTE: These must be synched with the command_function_map based on idx
        self._command_flag_map = {
            "class" : ["a","d","r"],
            "list"  : ["a","c","r","d"],
            "att"   : ["a","d","r"],
            "rel"   : ["a","d"],
            "save"  : [""],
            "load"  : [""],
            "exit"  : [""],
            "quit"  : [""],
            "help"  : [""]
        }
   
        #map relating commands to the names of methods that can be called on them
        #NOTE: these must be synched with command_flag_map based on idx
        self._command_function_map = {
            "class" : ["add_entity","delete_entity","rename_entity"],
            "list"  : ["list_everything","list_entities","list_relations","list_entity_details"],
            "att"   : ["add_attribute","delete_attribute","rename_attribute"],
            "rel"   : ["add_relation","delete_relation"],
            "save"  : ["save"],
            "load"  : ["load"],
            "exit"  : ["quit"],
            "quit"  : ["quit"],
            "help"  : ["help"]
        }
    
    def run(self) -> None:
        while not self._shouldQuit:
            s = Input.readLine()

            try:
                #parse the command
                input = self.parse(s)

                #return from input is [function object, arg1,...,argn]
                command = input[0]
                args = input[1:]

                #execute the command
                out = command(args)
            except Exception as e:
                Output.write(str(e))
            
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
        try:
            #actual input to be parsed, split on spaces
            bits = input.split()

            #Get the command that will be run 
            command_str = ""
            #list slicing generates an empty list instead of an IndexError
            command_str = self.__find_function(bits[0:1], bits[1:2])

            #Get the args that will be passed to that command
            args = []
            if not str(bits[1:2]).__contains__("-"):
                args = self.__check_args(bits[1:])
            else:
                args = self.__check_args(bits[2:])

            #Get the class the command is in
            command_class = self.__find_class(command_str)

            #go from knowing which class to having a specific instance
            #of the object that the method needs to be called on
            obj = self
            if command_class == Diagram:
                obj = self._diagram
            elif command_class == Entity:
                #if the method is in entity, get entity that needs to be changed
                obj = self._diagram.get_entity(args[0])
            elif command_class == Help:
                obj = Help
            
            #build and return the callable + args
            return [getattr(obj, command_str)] + args
        
        #This exception should be unreachable, it is here as a safeguard 
            #(and for easy testing)
        except Exception as e:
            return e

    def __check_args(self, args:list):
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
                raise CE.InvalidArgumentError(arg)
        return args

    def __find_function(self, command:list, flag:list = [""]):
        '''Finds the name of the function that should be called
        
            Args:
                command - the command that was given to the parser
                flag - the flag that was given to the parser
            
            Raises: 
                CustomExceptions.CommandNotFoundError if the command entered is
                    invalid
                CustomExceptions.InvalidFlagError if the flag entered is invalid
        
            Returns:
                The name of the function that needs to be called
        '''
        #convert the params to strings
        command = str(command[0])
        flag = str(flag[0]) if len(flag) > 0 else ""

        #check if the list of keys in the commmand flag map contains the given command
        command_list = list(self._command_flag_map.keys())
 
        valid_command = command_list.__contains__(command)
        if not valid_command:
            raise CE.CommandNotFoundError(command)
        
        #pull the list of flags for the validated command
        flag_list = self._command_flag_map[command]
        
        #Make sure that the flag is a flag (preceded with -)
        #some commands are just "command arg" so this needs to be checked
        prepped_flag = ""
        valid_flag = True
        if flag.__contains__("-"):
            prepped_flag = flag.lstrip("-")
            valid_flag = flag_list.__contains__(prepped_flag)
        
        if not valid_flag:
            raise CE.InvalidFlagError(flag, command)
        
        #compiling the correct location to index into the function map
        flag_index = flag_list.index(prepped_flag)
        flags = self._command_function_map.get(command)
        return flags[flag_index]
    
    def __find_class(self, function:str):
        '''Takes a function and locates the class that it exists in
        
            Args:
                function - the function to locate in a class
                
            Returns:
                the class the function originates in'''
        classes = [Diagram, Entity, Relation, Help]
        for cl in classes:
            if hasattr(cl, function):
                return cl
        
