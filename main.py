from PyQt6.QtWidgets import QApplication, QDialog

from umleditor.mvc_controller.cli_controller import CLI_Controller
from umleditor.mvc_view.gui_view.gui_lambda.GUIV2 import GUIV2
from umleditor.mvc_view.gui_view.gui_lambda.GUI3 import GUI3
from umleditor.mvc_view.gui_view.gui_cworld.view_GUI import ViewGUI
from umleditor.mvc_controller.gui_controller import ControllerGUI
from umleditor.mvc_controller.GUIV2_controller import ControllerGUI as ControllerGUIV2
from umleditor.mvc_view.gui_view.gui_lambda.versionDialog import VersionSelectionDialog
import sys


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
                controller = ControllerGUI(mainWindow)
            elif dialog.selected_version == "2":
                mainWindow = GUIV2()
                controller = ControllerGUIV2(mainWindow)
            elif dialog.selected_version == "3":
                mainWindow = GUI3()
            else:
                print("Invalid selection, defaulting to Gui V2.")
                mainWindow = GUIV3()

              # Ensure ControllerGUI is correctly initialized
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
