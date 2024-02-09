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

        self.save(answer)

    def save(self, name: str) -> bool:
        '''
        Saves the current diagram using a Serializer with the given filename

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

    def load(self, name: str) -> None:
        '''
        Loads a diagram with the given filename using a Serializer.

        #### Parameters:
        - `path` (str): The name of the file to be loaded.
        '''
        path = os.path.join(os.path.dirname(__file__), 'save')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name + '.json')
        loadedDiagram = Diagram()
        Serializer.deserialize(diagram=loadedDiagram, path=path)
        self._diagram = loadedDiagram
    
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
        cmd = CE.CommandNotFoundError(command)

        #if there is something in flags, chop a hyphen off the front.
        if len(flags) > 1 and flags[0] == "-":
            flag = flags[1:]
        else:
            flag = flags
        
        #sorting through by command, then flag, to figure out which method will be called.
        if "class" == command:
            if   flag == "a":
                cmd = self._diagram.add_entity
            elif flag == "d":
                cmd = self._diagram.delete_entity
            elif flag == "r":
                cmd = self._diagram.rename_entity
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "list" == command:
            if   flag == "a":
                cmd = self._diagram.list_everything
            elif flag == "c" and len(args) > 0:
                cmd = self._diagram.list_entity_details
            elif flag == "r":
                cmd = self._diagram.list_relations
            elif flag == "c": 
                cmd = self._diagram.list_entities           
            else:
                cmd = CE.InvalidFlagError(flag, command)
        
        elif "save" == command:
            if flag == "f":
                cmd = self.save
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "load" == command: 
            if flag == "f":
                cmd = self.load
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "att" == command:
            name = args.pop(0)
            entity = self._diagram.get_entity(name)
            if entity != None:
                if  flag == "a":
                    cmd = entity.add_attribute
                elif flag == "d":
                    cmd = entity.delete_attribute
                elif flag == "r":
                    cmd = entity.rename_attribute
                else:
                    cmd = CE.InvalidFlagError(flag, command)
            else:
                cmd = CE.EntityNotFoundError(name)

        elif "rel" == command:
            if  flag == "a":
                cmd = self._diagram.add_relation
            elif flag == "d":
                cmd = self._diagram.delete_relation
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "exit" == command or "quit" == command:
            if flag == "":
                cmd = self.quit
            else:
                cmd = CE.InvalidFlagError(flag, command)

        elif "help" == command:
            if len(flag) != 0:
                cmd = CE.InvalidFlagError(flag, command)
            else:
                cmd = Help.help



        return cmd
