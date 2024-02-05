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
    flag = args[0]  #renamed for readability

    if "class" == command:
        if   flag == "a":
            cmd = Diagram.addEntity
        elif flag == "d":
            cmd = Diagram.deleteEntity
        elif flag == "r":
            cmd = Entity.setName
        elif flag == "s":
            cmd = Controller.selectClass
        else:
            cmd = CE.InvalidFlagError(flag, command)

    elif "list" == command:
        if   flag == "a":
            cmd = None #TODO - List all classes and their attributes and relationships
        elif flag == "c":
            cmd = Diagram.listEntities
        elif flag == "r":
            cmd = None #TODO - List all relationships
        elif flag == "c" and len(args) > 1: #check if they put in a class name 
            cmd = None #TODO - List all data about a given class
        else:
            cmd = CE.InvalidFlagError(flag, command)
    
    elif "save" == command:
        if   flag == "n":
            cmd = None #TODO - the command for saving a file with a name
        else:
            cmd = CE.InvalidFlagError(flag, command)
    elif "load" == command:  #placeholder for eventual load flags - could be removed
       pass

    #all commands below this point require an active class
    elif Diagram.getClass() == None:
        cmd = CE.NoEntitySelected()

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
    
    return {cmd}
