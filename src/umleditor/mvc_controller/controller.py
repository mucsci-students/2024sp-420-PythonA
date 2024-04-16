from .controller_input import read_line
from .serializer import serialize, deserialize
from umleditor.mvc_controller.uml_parser import parse
from umleditor.mvc_model import CustomExceptions as CE
from umleditor.mvc_model.diagram import Diagram
from umleditor.mvc_controller.uml_parser import check_args
from umleditor.mvc_controller.momento import Momento
import os


class Controller:
    def __init__(self, d:Diagram = Diagram(), q:bool = False) -> None:
        self._should_quit = q
        self._diagram = d
        self.momento = Momento(self)
        self.command_count_tracker = 0

    def run(self, line: str) -> str:
        if len(line.strip()) > 0:
            try:
                # Parse the command
                input = parse(self, line)
                # The return from parse call is [function object, arg1,...,argn]
                command = input[0]
                args = input[1:]

                # Get the command name using the function's __name__ attribute
                command_name = command.__name__.lower() if hasattr(command, '__name__') else None

                # Check if the command is not one of the non-state-changing commands
                if command_name and command_name not in self.momento.non_state_changing_commands():
                    # Save the initial state and overwrite states everytime a valid command is taken.
                    self.momento.save_state(self.command_count_tracker)
                    self.command_count_tracker += 1

                # Execute the command
                return command(*args)

            except TypeError as t:
                self.command_count_tracker -= 1
                raise CE.InvalidArgCountError(t)
            except ValueError as v:
                self.command_count_tracker -= 1
                raise CE.NeedsMoreInput()
            except Exception as e:
                self.command_count_tracker -= 1
                raise e

    def undo(self):
        self.momento.save_state(self.command_count_tracker)
        if self.command_count_tracker > 0:
            self.command_count_tracker -= 1
            self.momento.load_state(self.command_count_tracker)

    def redo(self):
        self.command_count_tracker += 1
        self.momento.load_state(self.command_count_tracker)

    def quit(self):
        '''Basic Quit Routine. Prompts user to save, where to save, 
            validates input.
            
        Returns:
            If the name and filepath were valid or user doesn't want to save, returns true
            If name is invalid, returns invalid filename exception
            If filepath is invalid, returns invalid filepath exception
        '''
        # Remove all temp json state files
        self.momento.cleanup_states()
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
    
