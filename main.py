from PyQt6.QtWidgets import QApplication, QDialog

from umleditor.mvc_controller.cli_controller import CLI_Controller
from umleditor.mvc_view.gui_view.GUIV2 import GUIV2
from umleditor.mvc_view.gui_view.view_GUI import ViewGUI
from umleditor.mvc_controller.gui_controller import ControllerGUI
from umleditor.mvc_view.gui_view.versionDialog import VersionSelectionDialog
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
    app = QApplication(sys.argv)

    try:
        dialog = VersionSelectionDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            if dialog.selected_version == "1":
                mainWindow = ViewGUI()
            elif dialog.selected_version == "2":
                mainWindow = GUIV2()
            else:
                print("Invalid selection, defaulting to Gui V2.")
                mainWindow = GUIV2()

            controller = ControllerGUI(mainWindow)  # Ensure ControllerGUI is correctly initialized
            mainWindow.show()
            sys.exit(app.exec())
        else:
            print("No selection made, exiting.")
            sys.exit(0)
    except KeyboardInterrupt:
        # This handles ctrl+C gracefully
        print("\nApplication closed.")
    except Exception as e:
        # Generic exception handling
        print(f"Unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
