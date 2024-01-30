from Input import Input
from Output import Output

class Controller:
    def __init__(self) -> None:
        self.input = Input()
        self.output = Output()
        self.shouldQuit = False

    def run(self) -> None:
        while not self.shouldQuit:
            s = self.input.readLine()
            if s == 'quit' or s == 'exit':
                self.shouldQuit = True
            self.output.write('Last cmd: {}'.format(s))