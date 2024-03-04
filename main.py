from umleditor.mvc_controller.cli_controller import CLI_Controller
from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
from umleditor.mvc_controller.gui_controller import ControllerGUI
import sys
from PyQt6 import QtWidgets


def main():
    #decides which main to run
    if len(sys.argv) >= 2 and sys.argv[1] == 'cli':
        mainCLI()
    elif len(sys.argv) >= 2 and sys.argv[1] == 'debug':
        debug_main()
    else:
        mainGUI()

def debug_main():
    #CLI main without some error catching
    app = CLI_Controller()
    app.run()   

def mainCLI():
    #main CLI execution
    try:
        app = CLI_Controller()
        app.run()
    except KeyboardInterrupt:
        # This handles ctrl+C
        pass
    except EOFError:
        # This handles ctrl+D
        pass
    except Exception:
        # Never expect errors to be caught here
        print('Oh no! Unexpected Error!')


def mainGUI():
    #main gui execution
    try:
        # Create QApplication for running the program
        app = QtWidgets.QApplication(sys.argv)
        # Create an instance of our view and pass to controller
        mainWindow = ViewGUI()
        controller = ControllerGUI(mainWindow)
        # Set window to visible and start the application
        mainWindow.show()
        app.exec()
    except KeyboardInterrupt:
        # This handles ctrl+C
        pass
    except EOFError:
        # This handles ctrl+D
        pass
    except Exception:
        # Never expect errors to be caught here
        print('Oh no! Unexpected Error!')

if __name__ == '__main__':
    main()
