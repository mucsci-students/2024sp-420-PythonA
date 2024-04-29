import sys,os
from PyQt6.QtWidgets import QApplication, QDialog

from umleditor.mvc_controller.cli_controller import CLI_Controller
from umleditor.mvc_view.gui_view.gui_lambda.GUIV2 import GUIV2
from umleditor.mvc_view.gui_view.gui_lambda.GUI3 import GUI3
from umleditor.mvc_view.gui_view.gui_cworld.view_GUI import ViewGUI
from umleditor.mvc_controller.gui_controller import ControllerGUI
from umleditor.mvc_controller.GUIV2_controller import ControllerGUI as ControllerGUIV2
from umleditor.mvc_view.gui_view.gui_lambda.dialog_boxes.versionDialog import VersionSelectionDialog


class ApplicationFacade:
    def __init__(self):
        self.cli_app = CLI_Controller()

    def block_gui_terminal(self):
        # Blocks GUI from printing to the terminal
        sys.stdout = open(os.devnull, 'w')

    def run_cli(self):
        try:
            self.cli_app.run()
        except KeyboardInterrupt:
            # Handle ctrl+C gracefully
            pass
        except EOFError:
            # Handle ctrl+D gracefully
            pass
        except Exception as e:
            print(f"Oh no! Unexpected Error: {e}")

    def run_debug_cli(self):
        self.cli_app.run()  # Debug mode does not handle exceptions

    def run_gui(self):
        self.block_gui_terminal()
        app = QApplication(sys.argv)

        mainWindow = GUIV2()
        controller = ControllerGUIV2(mainWindow)
        mainWindow.show()
        sys.exit(app.exec())


    def main(self):
        if len(sys.argv) >= 2 and sys.argv[1] == 'cli':
            self.run_cli()
        elif len(sys.argv) >= 2 and sys.argv[1] == 'debug':
            self.run_debug_cli()
        else:
            self.run_gui()

if __name__ == '__main__':
    facade = ApplicationFacade()
    facade.main()