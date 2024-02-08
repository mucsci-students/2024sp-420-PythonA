from Controller import Controller

def main():
    app = Controller()
    app.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # This handles ctrl+C
        pass
    except Exception:
        # Never expect errors to be caught here
        print('Oh no! Unexpected Error!')