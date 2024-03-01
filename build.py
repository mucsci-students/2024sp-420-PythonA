import os

def main():
    if in_venv():
        os.system("pip install -e .")

def in_venv() -> bool:
    '''Checks if the user is currently in a virtual environment
    
        Return: 
            True - the user is in a venv or wants to continue outside one
            False - the user is not in a venv and doesn't want to continue
    '''
    venv_exists = True
    if not os.getenv("VIRTUAL_ENV"):
        print('''You are not currently in a virtual environment.
                 Running this script outside a virtual environment may not work as intended,
                 \t or may add files to user/system filepaths. For help setting up a venv, check the README.
                ''')
        venv_exists = True if input("Would you like to continue? Y/[N]: ").strip().lower()[0] == 'y' else False
    return venv_exists

if __name__ == '__main__':
    main()
        

