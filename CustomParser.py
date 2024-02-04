'''Parses commands, returning a function and a series of args to be given to that function as a list.'''
from CustomExceptions import CustomExceptions as CE
from Diagram import Diagram
from Entity import Entity
from Relation import Relation
import Controller


def parse (input:str) -> list:
    '''Parses a line of user input.
    
        Args:
            input(str) - the line to be parsed
        
        Return:
            With proper input: a list in the form [function, arg1,...,argN]
            With invalid name: CustomExceptions.InvalidArgumentError
            With invalid flag: CustomExceptions.InvalidFlagError
            With invalid command: CustomExceptions.CommandNotFoundError
    '''
    components = input.split(" ")
    try:
        __checkArgs(args=components[2:])
    except CE.InvalidArgumentError as e:
        return e
    return __findFunction(command=components[0], flags=components[1])


def __checkArgs(args:list):
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
            raise CE.InvalidArgumentError(arg)
     return None

def __findFunction(command:str, flags:str) -> function:
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
    
    args = list(flags[1:]) #start at 1 to skip the hyphen

    if "class" == command:
        if   args[0] == "a":
            cmd = Diagram.addEntity
        elif args[0] == "d":
            cmd = Diagram.deleteEntity
        elif args[0] == "r":
            cmd = Entity.setName
        elif args[0] == "s":
            cmd = Controller.selectClass
        else:
            cmd = CE.InvalidFlagError(args[0], command)
    
    elif"att" == command:
       pass
    
    elif"rel" == command:
       pass
    
    elif"list" == command:
       pass
    
    elif"save" == command:
       pass
    
    elif"load" == command:
       pass
    
    return {cmd}
