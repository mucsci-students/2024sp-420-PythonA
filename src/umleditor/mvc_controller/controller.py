from .controller_input import read_line
import umleditor.mvc_controller.controller_output as controller_output
from .serializer import CustomJSONEncoder, serialize, deserialize
from umleditor.mvc_controller.uml_parser import parse
from umleditor.mvc_model import CustomExceptions as CE
from umleditor.mvc_model.diagram import Diagram
from umleditor.mvc_controller.uml_parser import check_args
import os
import sys

class Controller:
    def __init__(self, d:Diagram = Diagram(), q:bool = False) -> None:
        self._should_quit = q
        self._diagram = d

    def run(self, line:str) -> str:
        if len(line.strip()) > 0:
            try:
                #parse the command
                input = parse(self, line)

                #return from input is [function object, arg1,...,argn]
                command = input[0]
                args = input[1:]

                #execute the command
                return command(*args)
            
            except TypeError as t:
                raise CE.InvalidArgCountError(t)
            except ValueError as v:
                print(str(v))
            except Exception as e:
                raise e

    def quit(self):
        '''Basic Quit Routine. Prompts user to save, where to save, 
            validates input.
            
        Returns:
            If the name and filepath were valid or user doesn't want to save, returns true
            If name is invalid, returns invalid filename exception
            If filepath is invalid, returns invalid filepath exception
        '''
        self._should_quit = True
        while True:
            answer = read_line('Would you like to save before quit? [Y]/n: ').strip()
            if not answer or answer in ['Y', 'n']: # default or Y/n
                break
        if answer == 'n':
            #user wants to quit without saving
            return
        else:
            answer = read_line('Name of file to save: ')

        if isinstance(check_args([answer]), Exception):
            return CE.IOFailedError("Save", "invalid filename")

        self.save(answer)

    def save(self, name: str) -> None:
        '''
        Saves the current diagram using a serializer with the given filename

        #### Parameters:
        - `name` (str): The name of the file to be saved.
        '''
        path = os.path.join(os.path.dirname(__file__), '../', '../', '../', 'save')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name + '.json')
        serialize(diagram=self._diagram, path=path)

    def load(self, name: str) -> None:
        '''
        Loads a diagram with the given filename using a deserializer.

        #### Parameters:
        - `path` (str): The name of the file to be loaded.
        '''
        path = os.path.join(os.path.dirname(__file__), '../', '../', '../', 'save')
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, name + '.json')
        loadedDiagram = Diagram()
        deserialize(diagram=loadedDiagram, path=path)
        self._diagram = loadedDiagram
    
