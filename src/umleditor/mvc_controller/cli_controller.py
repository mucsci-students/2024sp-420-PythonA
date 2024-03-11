from umleditor.mvc_controller.controller import Controller
import umleditor.mvc_controller.controller_output as controller_output
from umleditor.mvc_controller.controller_input import read_line
from umleditor.mvc_model.diagram import Diagram

class CLI_Controller (Controller):
    def __init__(self):
        super().__init__()

    def run(self):
        while self._should_quit == False:
            try:
                out = super().run(read_line())
                if out != None:
                    controller_output.write(out)
            except Exception as e: 
                controller_output.write(e)