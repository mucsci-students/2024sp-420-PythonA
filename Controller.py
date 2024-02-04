from Input import Input
from Output import Output
from Serializer import Serializer
from Diagram import Diagram

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
            if s == 'quit' or s == 'exit':
                self._shouldQuit = True
            self._output.write('Last cmd: {}'.format(s))
        
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