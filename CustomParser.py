'''Parses commands, returning a function and a series of args to be given to that function as a list.'''
from CustomExceptions import CustomExceptions #for CommandNotFoundError
from Diagram import Diagram
from Entity import Entity
from Relation import Relation
import Controller


def parse (input:str) -> list:
    components = input.split(" ")
    func = __findFunction(components[0], components[1])



def __findFunction(command:str, flags:str) -> function:
    '''Given a command and flags, finds and returns the appropriate function
        
        Args: 
            command(str): the command to be used (ex: class)
            flags(str): the block after the command, begins with a hyphen
            
        Return: a function object that should be called
    '''
    cmd = CustomExceptions.CommandNotFoundError(command)
    #skip the hyphen
    args = flags[1].split()

    if "class" == command:
        if   args[0] == "a":
           cmd = {Diagram.addEntity}
        elif args[0] == "d":
            cmd = {Diagram.deleteEntity}
        elif args[0] == "r":
            cmd = {Entity.setName}
        elif args[0] == "s":
            cmd = {Controller.selectClass}
    
    elif"att" == command:
       
    
    elif"rel" == command:
       
    
    elif"list" == command:
       
    elif"save" == command:
       
    
    elif"load" == command:
       
