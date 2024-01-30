from Input import Input
from Output import Output
from Diagram import Diagram

class Controller:
    def __init__(self) -> None:
        self._input = Input()
        self._output = Output()
        self._shouldQuit = False
        self._diagram = Diagram()

    def run(self) -> None:
        while not self._shouldQuit:
            s = self._input.readLine()
            if s == 'quit' or s == 'exit':
                self._shouldQuit = True
            self._output.write('Last cmd: {}'.format(s))