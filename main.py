import sys, os
from PyQt6.QtWidgets import QApplication, QDialog

from umleditor.mvc_controller.cli_controller import CLI_Controller
from umleditor.mvc_view.gui_view.gui_lambda.GUIV2 import GUIV2
import sys


def main():
    # decides which main to run
    if len(sys.argv) >= 2 and sys.argv[1] == 'cli':
        mainCLI()
    elif len(sys.argv) >= 2 and sys.argv[1] == 'debug':
        debug_main()
    else:
        mainGUI()


def blockGuiTerminal():
    # will not print anything to the terminal
    sys.stdout = open(os.devnull, 'w')


def debug_main():
    # CLI main without some error catching
    app = CLI_Controller()
    app.run()


def mainCLI():
    # main CLI execution
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
    blockGuiTerminal()
    app = QApplication(sys.argv)

    mainWindow = GUIV2()

    # Ensure ControllerGUI is correctly initialized
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
