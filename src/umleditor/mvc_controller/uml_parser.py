from umleditor.mvc_model import CustomExceptions as CE
from .uml_lexer import lex_input as lex
from umleditor.mvc_model import *

import re

#list of all classes that need to be searched for commands
classes = [Diagram, Entity, Relation, help_command]


def parse (c, input:str) -> list:
    '''Parses a line of user input.
    
        Args:
            c - the controller that owns the diagram being modified
            input(str) - the line to be parsed
        
        Return:
            With proper input: a list in the form [function, arg1,...,argN]
            With invalid name: CustomExceptions.InvalidArgumentError
            With invalid flag: CustomExceptions.InvalidFlagError
            With invalid command: CustomExceptions.CommandNotFoundError
    '''
    
    #actual input to be parsed, split on spaces
    bits = input.split()

    #Get the command that will be run 
    command_str = ""
    #list slicing generates an empty list instead of an IndexError
    command_str = lex(bits[0:1], bits[1:2])
    #Get the args that will be passed to that command
    args = []
    if not str(bits[1:2]).__contains__("-"):
        args = check_args(bits[1:])
    else:
        args = check_args(bits[2:])

    #Get the class the command is in
    command_class = __find_class(command_str)

    #go from knowing which class to having a specific instance
    #of the class that the method needs to be called on
    obj = c
    if command_class == Diagram:
        obj = c._diagram
    elif command_class == Entity:
        #if no args were provided, no entity can be found. Generate an error about invalid args
        if not args:
            raise CE.NeedsMoreInput()
        
        #if the method is in entity, get entity that needs to be changed
            #pop the first element of args because it is the entity name, not a method param
        obj = c._diagram.get_entity(args.pop(0))
    elif command_class == help_command:
        obj = help_command
    
    #build and return the callable + args
    return [getattr(obj, command_str)] + args

def __find_class(function:str):
    '''Takes a function and locates the class that it exists in
    
        Args:
            function - the function to locate in a class
            
        Returns:
            the class the function originates in'''
    for cl in classes:
        if hasattr(cl, function):
            return cl
        
def check_args(args:list):
    '''Given a list of args, checks to make sure each one is valid. 
        Valid includes alphanumeric, -, and _.
        
        Args: 
            args(list): a list of strings to be checked
            
        Return: 
            CustomExceptions.InvalidArgumentError if an argument provided is invalid
            The list of args provided if all args are valid
    '''
    exp = re.compile('[^a-zA-Z-_0-9]')
    for arg in args:
        if len(exp.findall(arg)) > 0:
            raise CE.InvalidArgumentError(arg)
    return args
