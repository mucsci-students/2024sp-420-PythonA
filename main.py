import sys,os
from PyQt6.QtWidgets import QApplication, QDialog

from umleditor.mvc_controller.cli_controller import CLI_Controller
from umleditor.mvc_view.gui_view.gui_lambda.GUIV2 import GUIV2
from umleditor.mvc_view.gui_view.gui_lambda.GUI3 import GUI3
from umleditor.mvc_view.gui_view.gui_cworld.view_GUI import ViewGUI
from umleditor.mvc_controller.gui_controller import ControllerGUI
from umleditor.mvc_controller.GUIV2_controller import ControllerGUI as ControllerGUIV2
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.versionDialog import VersionSelectionDialog


class Command:
    def execute(self):
        pass


class RunCLICommand(Command):
    def __init__(self, cli_app):
        self.cli_app = cli_app

    def execute(self):
        try:
            self.cli_app.run()
        except KeyboardInterrupt:
            pass
        except EOFError:
            pass
        except Exception as e:
            print(f"Unexpected Error: {e}")


class RunDebugCLICommand(Command):
    def __init__(self, cli_app):
        self.cli_app = cli_app

    def execute(self):
        self.cli_app.run()  # Debug mode does not handle exceptions


class RunGUICommand(Command):
    def execute(self):
        sys.stdout = open(os.devnull, 'w')  # Block GUI from printing to the terminal
        app = QApplication(sys.argv)
        mainWindow = GUIV2()
        controller = ControllerGUIV2(mainWindow)
        mainWindow.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    cli_app = CLI_Controller()
    commands = {
        "cli": RunCLICommand(cli_app),
        "debug": RunDebugCLICommand(cli_app),
        "gui": RunGUICommand()
    }
    mode = sys.argv[1] if len(sys.argv) > 1 else "gui"
    commands[mode].execute()