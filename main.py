# from Controller import Controller
# from umleditor.mvc_controller.controller import Controller
from umleditor.mvc_controller import Controller

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

if __name__ == '__main__':
    if not __debug__:
        debug_main()
    else:
        main()