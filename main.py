from umleditor.mvc_controller import Controller
from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
from umleditor.mvc_controller.controller_GUI import ControllerGUI
import sys
from PyQt6 import QtWidgets

def debug_main():
    app = Controller()
    app.run()

def main():
    try:
        app = Controller()
        app.run()
    except KeyboardInterrupt:
        # This handles ctrl+C
        pass
    except EOFError:
        # This handles ctrl+D
        pass
    except Exception as e:
        # Never expect errors to be caught here
        print('Oh no! Unexpected Error!')

def mainGUI():
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
    except Exception as e:
        # Never expect errors to be caught here
        print('Oh no! Unexpected Error!')

if __name__ == '__main__':
    if not __debug__:
        debug_main()
    else:
        #main()
        mainGUI()